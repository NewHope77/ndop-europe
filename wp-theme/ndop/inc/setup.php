<?php
/**
 * One-time migration: the movement's photographs into the media library, and
 * its six pages into WordPress.
 *
 * Written as part of the theme rather than performed by hand in the admin so
 * that the move can be repeated exactly — once on the temporary address while
 * the site is being built, and again on nationaldayofprayer.eu when it goes
 * live, with the same result both times.
 *
 * It is safe to run twice. Nothing is overwritten: a photograph already in the
 * library is reused, and a page that already exists is left exactly as the
 * client last saved it.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const NDOP_IMPORT_FLAG = 'ndop_imported_version';
const NDOP_SOURCE_META = '_ndop_source_file';

/** Slug => the page's title and the order it sits in the admin list. */
function ndop_pages() {
	return array(
		'index'     => 'Home',
		'about'     => 'About Us',
		'history'   => 'History',
		'resources' => 'Resources & Legal Base',
		'faq'       => 'FAQ',
		'contact'   => 'Contact',
	);
}

add_action( 'after_switch_theme', 'ndop_install' );

/**
 * Build the site. Returns a line-by-line account of what it did, which the
 * admin notice and the Tools screen both show.
 *
 * With $replace the stored pages are written over with the originals from the
 * theme. That is for putting a correction into a page nobody has edited yet;
 * it discards whatever is in the editor, so nothing calls it on its own.
 */
function ndop_install( $replace = false ) {
	$log = array();

	require_once ABSPATH . 'wp-admin/includes/image.php';
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';

	$created = 0;
	$kept    = 0;

	foreach ( ndop_pages() as $slug => $title ) {
		$markup = ndop_page_markup( $slug );
		if ( null === $markup ) {
			$log[] = sprintf( 'skipped %s — no content file in the theme yet', $slug );
			continue;
		}

		$existing = get_page_by_path( $slug );
		if ( $existing instanceof WP_Post ) {
			if ( ! $replace ) {
				$kept++;
				$log[] = sprintf( 'kept %s — the page already exists, nothing overwritten', $slug );
				continue;
			}

			wp_update_post( array( 'ID' => $existing->ID, 'post_content' => $markup ) );
			$log[] = sprintf( 'replaced %s with the version from the theme', $slug );
			continue;
		}

		$id = wp_insert_post( array(
			'post_type'    => 'page',
			'post_status'  => 'publish',
			'post_title'   => $title,
			'post_name'    => $slug,
			'post_content' => $markup,
		), true );

		if ( is_wp_error( $id ) ) {
			$log[] = sprintf( 'failed %s — %s', $slug, $id->get_error_message() );
			continue;
		}

		$created++;
		$log[] = sprintf( 'created %s', $slug );
	}

	// The home page is a page, not a list of posts.
	$home = get_page_by_path( 'index' );
	if ( $home instanceof WP_Post ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $home->ID );
		$log[] = 'set the home page';
	}

	// Addresses as /about/ rather than /?page_id=7.
	if ( '/%postname%/' !== get_option( 'permalink_structure' ) ) {
		global $wp_rewrite;
		$wp_rewrite->set_permalink_structure( '/%postname%/' );
		$wp_rewrite->flush_rules();
		$log[] = 'switched the addresses to readable form';
	}

	update_option( 'blogname', 'The National Days of Prayer Movement in Europe' );
	update_option( 'blogdescription', 'A movement encouraging the establishment of a National Day of Prayer at the country level in every European country.' );

	update_option( NDOP_IMPORT_FLAG, NDOP_VERSION );
	set_transient( 'ndop_install_log', $log, DAY_IN_SECONDS );

	return $log;
}

/**
 * The stored block markup for one page, with every photograph resolved to the
 * copy now sitting in the media library.
 */
function ndop_page_markup( $slug ) {
	$file = get_theme_file_path( 'pages/' . $slug . '.html' );
	if ( ! file_exists( $file ) ) {
		return null;
	}

	$markup = (string) file_get_contents( $file );

	// Each placeholder names a file in assets/img; import it once, then write
	// its real address and id into the block.
	if ( preg_match_all( '/__IMG_(?:URL|ID):([A-Za-z0-9._-]+)__/', $markup, $m ) ) {
		foreach ( array_unique( $m[1] ) as $name ) {
			$id = ndop_import_image( $name );
			if ( ! $id ) {
				continue;
			}
			$markup = str_replace( '__IMG_ID:' . $name . '__', (string) $id, $markup );
			$markup = str_replace( '__IMG_URL:' . $name . '__', wp_get_attachment_url( $id ), $markup );
		}
	}

	return $markup;
}

/**
 * A photograph from the theme, placed in the media library.
 *
 * The file name is recorded against the attachment, so running this a second
 * time finds the existing copy instead of making a duplicate.
 */
function ndop_import_image( $name ) {
	$found = get_posts( array(
		'post_type'      => 'attachment',
		'post_status'    => 'inherit',
		'posts_per_page' => 1,
		'fields'         => 'ids',
		'meta_key'       => NDOP_SOURCE_META,
		'meta_value'     => $name,
	) );
	if ( ! empty( $found ) ) {
		ndop_ensure_caption( (int) $found[0], $name );
		return (int) $found[0];
	}

	$source = get_theme_file_path( 'assets/img/' . $name );
	if ( ! file_exists( $source ) ) {
		return 0;
	}

	$upload = wp_upload_bits( $name, null, (string) file_get_contents( $source ) );
	if ( ! empty( $upload['error'] ) ) {
		return 0;
	}

	$captions = ndop_caption_map();

	$type = wp_check_filetype( $upload['file'] );
	$id   = wp_insert_attachment( array(
		'post_mime_type' => $type['type'],
		'post_title'     => ndop_image_title( $name ),
		'post_status'    => 'inherit',
		// The line shown when the picture is opened full size. It lives with
		// the picture, so the client changes it in the media library.
		'post_excerpt'   => isset( $captions[ $name ] ) ? $captions[ $name ] : '',
	), $upload['file'] );

	if ( is_wp_error( $id ) || ! $id ) {
		return 0;
	}

	wp_update_attachment_metadata( $id, wp_generate_attachment_metadata( $id, $upload['file'] ) );
	update_post_meta( $id, NDOP_SOURCE_META, $name );

	return (int) $id;
}

/**
 * Give a picture already in the library its caption, if it has none.
 *
 * Only fills a blank: a caption the client has written is theirs, and a second
 * run must not undo it.
 */
function ndop_ensure_caption( $id, $name ) {
	$captions = ndop_caption_map();
	if ( empty( $captions[ $name ] ) ) {
		return;
	}

	$post = get_post( $id );
	if ( $post instanceof WP_Post && '' === trim( (string) $post->post_excerpt ) ) {
		wp_update_post( array( 'ID' => $id, 'post_excerpt' => $captions[ $name ] ) );
	}
}

/** "reagan-signing.jpg" reads better in the library as "Reagan signing". */
function ndop_image_title( $name ) {
	$base = preg_replace( '/\.[a-z0-9]+$/i', '', $name );
	return ucfirst( str_replace( array( '-', '_' ), ' ', $base ) );
}
