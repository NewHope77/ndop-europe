<?php
/**
 * The site's fixed navigation.
 *
 * Six pages that do not change, so the order is declared here rather than
 * assembled from a WordPress menu. That keeps the client out of a screen where
 * one wrong drag reorders the site, and keeps data-nav in step with the slugs
 * the script matches against.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Slug => label, in the order they appear in the masthead. */
function ndop_nav_items() {
	return array(
		'index'     => 'Home',
		'about'     => 'About Us',
		'history'   => 'History',
		'resources' => 'Resources & Legal Base',
		'faq'       => 'FAQ',
		'contact'   => 'Contact',
	);
}

/**
 * Address of one of those pages.
 *
 * Falls back to /slug/ when the page has not been created yet, so a half-built
 * site still links somewhere sensible instead of to the home page.
 */
function ndop_page_url( $slug ) {
	if ( 'index' === $slug ) {
		return home_url( '/' );
	}

	$page = get_page_by_path( $slug );
	if ( $page instanceof WP_Post ) {
		return get_permalink( $page );
	}

	return home_url( '/' . $slug . '/' );
}
