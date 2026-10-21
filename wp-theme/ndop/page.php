<?php
/**
 * Every page of the site.
 *
 * The content is printed with no wrapper of its own: each section in the
 * editor already carries .section and .wrap, exactly as in the static build,
 * so an extra container here would change the layout. The page's heading is
 * part of its first section, which is why the title is not printed separately.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

while ( have_posts() ) {
	the_post();
	the_content();
}

get_footer();
