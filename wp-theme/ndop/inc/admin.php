<?php
/**
 * What the theme reports to whoever is administering the site.
 *
 * Only two things: what the migration did when the theme was switched on, and
 * a way to run it again if a page was deleted by accident.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'admin_notices', 'ndop_install_notice' );
function ndop_install_notice() {
	$log = get_transient( 'ndop_install_log' );
	if ( empty( $log ) || ! current_user_can( 'manage_options' ) ) {
		return;
	}
	delete_transient( 'ndop_install_log' );
	?>
	<div class="notice notice-success is-dismissible">
		<p><strong><?php esc_html_e( 'NDOP Europe is set up.', 'ndop' ); ?></strong></p>
		<ul style="margin:.4em 0 .8em 1.4em;list-style:disc">
			<?php foreach ( $log as $line ) : ?>
				<li><?php echo esc_html( $line ); ?></li>
			<?php endforeach; ?>
		</ul>
	</div>
	<?php
}

add_action( 'admin_menu', 'ndop_tools_page' );
function ndop_tools_page() {
	add_management_page(
		__( 'NDOP content', 'ndop' ),
		__( 'NDOP content', 'ndop' ),
		'manage_options',
		'ndop-content',
		'ndop_render_tools_page'
	);
}

function ndop_render_tools_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$log = array();
	if ( isset( $_POST['ndop_rebuild'] ) && check_admin_referer( 'ndop_rebuild' ) ) {
		$log = (array) ndop_install( false );
	}
	if ( isset( $_POST['ndop_replace'] ) && check_admin_referer( 'ndop_rebuild' ) ) {
		if ( empty( $_POST['ndop_confirm'] ) ) {
			$log = array( 'nothing done — tick the box first, so this cannot happen by a stray click' );
		} else {
			$log = (array) ndop_install( true );
		}
	}
	?>
	<div class="wrap">
		<h1><?php esc_html_e( 'NDOP content', 'ndop' ); ?></h1>
		<p>
			<?php esc_html_e( 'Recreates any of the six pages that is missing and makes sure every photograph from the brochure is in the media library.', 'ndop' ); ?>
			<strong><?php esc_html_e( 'Pages that already exist are never touched', 'ndop' ); ?></strong>
			<?php esc_html_e( '— edits made in the editor are safe.', 'ndop' ); ?>
		</p>

		<?php if ( $log ) : ?>
			<div class="notice notice-info"><ul style="margin:.6em 0 .6em 1.4em;list-style:disc">
				<?php foreach ( $log as $line ) : ?>
					<li><?php echo esc_html( $line ); ?></li>
				<?php endforeach; ?>
			</ul></div>
		<?php endif; ?>

		<form method="post">
			<?php wp_nonce_field( 'ndop_rebuild' ); ?>
			<p><button class="button button-primary" name="ndop_rebuild" value="1"><?php esc_html_e( 'Check the pages and images', 'ndop' ); ?></button></p>

			<hr>

			<h2><?php esc_html_e( 'Start the pages again', 'ndop' ); ?></h2>
			<p>
				<?php esc_html_e( 'Writes every page back to the version that ships with the theme.', 'ndop' ); ?>
				<strong><?php esc_html_e( 'Anything edited in the editor is lost.', 'ndop' ); ?></strong>
				<?php esc_html_e( 'This is here for applying a correction while the site is still being built.', 'ndop' ); ?>
			</p>
			<p>
				<label>
					<input type="checkbox" name="ndop_confirm" value="1">
					<?php esc_html_e( 'Yes — discard any edits and use the theme\'s version', 'ndop' ); ?>
				</label>
			</p>
			<p>
				<button class="button button-link-delete" name="ndop_replace" value="1">
					<?php esc_html_e( 'Replace the pages with the originals', 'ndop' ); ?>
				</button>
			</p>
		</form>
	</div>
	<?php
}
