<?php
/**
 * A missing address. Kept in the site's own design rather than the browser's
 * default, with a way back rather than a dead end.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>
<section class="page-hero">
  <div class="page-hero__map" aria-hidden="true"></div>
  <div class="wrap page-hero__inner">
    <h1>This page could not be found</h1>
    <p class="lede">The address may have changed, or it was mistyped.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="btn-row">
      <a class="btn btn--primary" href="<?php echo esc_url( home_url( '/' ) ); ?>">Back to the home page</a>
      <a class="btn" href="<?php echo esc_url( ndop_page_url( 'contact' ) ); ?>">Contact the movement</a>
    </div>
  </div>
</section>
<?php
get_footer();
