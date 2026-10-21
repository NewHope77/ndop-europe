<?php
/**
 * NDOP Europe — theme setup.
 *
 * The design system lives in assets/css/style.css and is shared, unchanged,
 * with the static build this site grew out of. Nothing here restyles anything;
 * this file only wires that stylesheet, the behaviour script and the editor
 * into WordPress.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'NDOP_VERSION', '1.0.0' );

/* -------------------------------------------------------------------------
 * Theme support
 * ---------------------------------------------------------------------- */

add_action( 'after_setup_theme', 'ndop_setup' );
function ndop_setup() {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'html5', array(
		'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script',
	) );

	// Colours, spacing and type are declared in theme.json, which is also what
	// stops WordPress wrapping every group in a second div and flattening the
	// grids this design is built from. Do not move them back here.

	register_nav_menus( array(
		'primary' => __( 'Primary navigation', 'ndop' ),
	) );
}

/* -------------------------------------------------------------------------
 * Front-end assets
 * ---------------------------------------------------------------------- */

add_action( 'wp_enqueue_scripts', 'ndop_assets' );
function ndop_assets() {
	wp_enqueue_style(
		'ndop-fonts',
		'https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600;700&display=swap',
		array(),
		null
	);

	// Versioned by file contents, so a changed stylesheet can never be served
	// from a stale browser cache.
	wp_enqueue_style(
		'ndop-style',
		get_theme_file_uri( 'assets/css/style.css' ),
		array( 'ndop-fonts' ),
		ndop_asset_version( 'assets/css/style.css' )
	);

	// Only what WordPress's own markup makes necessary — see the file's header.
	wp_enqueue_style(
		'ndop-wp',
		get_theme_file_uri( 'assets/css/wp.css' ),
		array( 'ndop-style' ),
		ndop_asset_version( 'assets/css/wp.css' )
	);

	wp_enqueue_script(
		'ndop-main',
		get_theme_file_uri( 'assets/js/main.js' ),
		array(),
		ndop_asset_version( 'assets/js/main.js' ),
		true
	);

	// The block editor's own stylesheet fights nothing here, but the theme has
	// no use for the global-styles layer WordPress injects for block themes.
	wp_dequeue_style( 'wp-block-library-theme' );
}

/** Content hash of a theme file, so caches break exactly when the file changes. */
function ndop_asset_version( $relative ) {
	$path = get_theme_file_path( $relative );
	return file_exists( $path ) ? substr( md5_file( $path ), 0, 8 ) : NDOP_VERSION;
}

/* -------------------------------------------------------------------------
 * The theme choice must be applied before the first paint
 * ---------------------------------------------------------------------- */

add_action( 'wp_head', 'ndop_theme_preference', 2 );
function ndop_theme_preference() {
	?>
<meta name="theme-color" content="#0C335B" id="themeColor">
<link rel="icon" href="<?php echo esc_url( get_theme_file_uri( 'assets/img/favicon.svg' ) ); ?>" type="image/svg+xml">
<script>
  // Without this a dark-theme visitor sees a white flash on every page.
  (function () {
    try {
      var t = localStorage.getItem('ndop.theme');
      if (t === 'dark' || t === 'light') document.documentElement.setAttribute('data-theme', t);
    } catch (e) { /* private browsing */ }
  })();
</script>
	<?php
}

/* -------------------------------------------------------------------------
 * Search-engine metadata
 *
 * Written here rather than delegated to an SEO plugin: the site has six fixed
 * pages, and a plugin would add an admin surface the client does not need.
 * ---------------------------------------------------------------------- */

add_action( 'wp_head', 'ndop_meta', 3 );
function ndop_meta() {
	$description = ndop_description();
	$canonical   = is_front_page() ? home_url( '/' ) : get_permalink();
	$image       = get_theme_file_uri( 'assets/img/hero-europe-cross.jpg' );
	?>
<meta name="description" content="<?php echo esc_attr( $description ); ?>">
<link rel="canonical" href="<?php echo esc_url( $canonical ); ?>">
<meta property="og:type" content="website">
<meta property="og:site_name" content="<?php echo esc_attr( get_bloginfo( 'name' ) ); ?>">
<meta property="og:title" content="<?php echo esc_attr( wp_get_document_title() ); ?>">
<meta property="og:description" content="<?php echo esc_attr( $description ); ?>">
<meta property="og:image" content="<?php echo esc_url( $image ); ?>">
<meta property="og:locale" content="en">
<meta name="twitter:card" content="summary_large_image">
	<?php
	if ( is_front_page() ) {
		$schema = array(
			'@context'    => 'https://schema.org',
			'@type'       => 'Organization',
			'name'        => get_bloginfo( 'name' ),
			'url'         => home_url( '/' ),
			'description' => 'A movement encouraging the establishment of a National Day of Prayer at the country level in every European country.',
			'areaServed'  => 'Europe',
			'email'       => ndop_email(),
		);
		echo "\n" . '<script type="application/ld+json">' . wp_json_encode( $schema ) . '</script>' . "\n";
	}
}

/**
 * The page's own title, exactly as it was written.
 *
 * Left to itself WordPress builds "About Us – site name". The pages carry
 * titles chosen for how they read in a search result, so those are used
 * instead; anything outside the six falls back to WordPress's own.
 */
add_filter( 'pre_get_document_title', 'ndop_document_title' );
function ndop_document_title( $title ) {
	$meta = ndop_meta_for_current_page();
	return $meta ? $meta['title'] : $title;
}

/** The page's own summary, falling back to the movement's one-line description. */
function ndop_description() {
	$meta = ndop_meta_for_current_page();
	if ( $meta ) {
		return $meta['description'];
	}

	if ( is_singular() ) {
		$post = get_queried_object();
		if ( $post instanceof WP_Post && '' !== trim( (string) $post->post_excerpt ) ) {
			return wp_strip_all_tags( $post->post_excerpt );
		}
	}
	return get_bloginfo( 'description' )
		?: 'A movement encouraging the establishment of a National Day of Prayer at the country level in every European country.';
}

/** The stored title and description of the page being shown, if it is one of ours. */
function ndop_meta_for_current_page() {
	if ( ! is_singular( 'page' ) && ! is_front_page() ) {
		return null;
	}

	$map  = ndop_meta_map();
	$slug = ndop_current_page_slug();

	return isset( $map[ $slug ] ) ? $map[ $slug ] : null;
}

/** The movement's address, in one place so it is changed once. */
function ndop_email() {
	return 'info@nationaldayofprayer.eu';
}

/* -------------------------------------------------------------------------
 * Body attributes the stylesheet and script rely on
 * ---------------------------------------------------------------------- */

add_filter( 'body_class', 'ndop_body_class' );
function ndop_body_class( $classes ) {
	$classes[] = 'ndop';
	return $classes;
}

/**
 * main.js marks the current navigation item from data-page on <body>.
 * The slug of the page carries that value; the front page is "index".
 */
function ndop_current_page_slug() {
	if ( is_front_page() ) {
		return 'index';
	}
	$post = get_queried_object();
	return ( $post instanceof WP_Post ) ? $post->post_name : '';
}

/* -------------------------------------------------------------------------
 * Pictures that open full size
 *
 * The attribute the viewer script looks for is added here rather than stored
 * in the page. A core/image block has to be saved exactly as the block itself
 * would save it — anything extra and the client is told the page contains
 * invalid content. So a container asks for the behaviour with the class
 * is-zoomable, and the images inside it are marked as the page is rendered.
 * ---------------------------------------------------------------------- */

add_filter( 'render_block_core/group', 'ndop_mark_zoomable_images', 10, 2 );
function ndop_mark_zoomable_images( $content, $block ) {
	$classes = isset( $block['attrs']['className'] ) ? $block['attrs']['className'] : '';
	if ( false === strpos( $classes, 'is-zoomable' ) ) {
		return $content;
	}

	if ( ! class_exists( 'WP_HTML_Tag_Processor' ) ) {
		return $content;
	}

	$html = new WP_HTML_Tag_Processor( $content );
	while ( $html->next_tag( 'img' ) ) {
		$html->set_attribute( 'data-lightbox', '' );

		$caption = ndop_image_caption( (string) $html->get_attribute( 'class' ) );
		if ( '' === $caption ) {
			$caption = (string) $html->get_attribute( 'alt' );
		}
		if ( '' !== $caption ) {
			$html->set_attribute( 'data-caption', $caption );
		}
	}

	return $html->get_updated_html();
}

/** The caption stored with the picture, found from the wp-image-NN class. */
function ndop_image_caption( $class_attribute ) {
	if ( ! preg_match( '/wp-image-(\d+)/', $class_attribute, $m ) ) {
		return '';
	}
	return (string) wp_get_attachment_caption( (int) $m[1] );
}

/* -------------------------------------------------------------------------
 * Editor
 * ---------------------------------------------------------------------- */

add_action( 'after_setup_theme', 'ndop_editor_styles' );
function ndop_editor_styles() {
	add_theme_support( 'editor-styles' );
	add_editor_style( array(
		'assets/css/style.css',
		'assets/css/wp.css',
		'assets/css/editor.css',
	) );
}

require_once get_theme_file_path( 'inc/meta.php' );
require_once get_theme_file_path( 'inc/captions.php' );
require_once get_theme_file_path( 'inc/options.php' );
require_once get_theme_file_path( 'inc/navigation.php' );
require_once get_theme_file_path( 'inc/patterns.php' );
require_once get_theme_file_path( 'inc/setup.php' );
require_once get_theme_file_path( 'inc/admin.php' );
