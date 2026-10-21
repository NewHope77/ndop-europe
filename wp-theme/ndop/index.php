<?php
/**
 * WordPress requires this file. The site is six fixed pages with no blog, so
 * nothing should ever reach it; if something does, say so plainly rather than
 * printing an empty listing.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>
<section class="page-hero">
  <div class="page-hero__map" aria-hidden="true"></div>
  <div class="wrap page-hero__inner">
    <h1>Nothing here</h1>
    <p class="lede">This address does not match a page of the site.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p><a class="btn btn--primary" href="<?php echo esc_url( home_url( '/' ) ); ?>">Back to the home page</a></p>
  </div>
</section>
<?php
get_footer();
