<?php
/**
 * The home page. Identical handling to any other page — it is singled out only
 * so WordPress does not fall through to the blog listing.
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
