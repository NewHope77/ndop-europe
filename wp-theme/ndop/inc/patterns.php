<?php
/**
 * Sections the client can insert into a page.
 *
 * The six pages ship complete, so nothing here is needed to see the site. These
 * are for later: a new section added to an existing page, laid out correctly
 * from the first click instead of assembled out of bare blocks.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'init', 'ndop_register_patterns' );
function ndop_register_patterns() {
	if ( ! function_exists( 'register_block_pattern_category' ) ) {
		return;
	}

	register_block_pattern_category( 'ndop', array(
		'label' => __( 'Movement sections', 'ndop' ),
	) );

	register_block_pattern( 'ndop/text-section', array(
		'title'      => __( 'Text section', 'ndop' ),
		'categories' => array( 'ndop' ),
		'content'    => '<!-- wp:group {"tagName":"section","className":"section"} -->
<section class="wp-block-group section">
<!-- wp:group {"className":"wrap"} -->
<div class="wp-block-group wrap">
<!-- wp:group {"className":"section-head reveal"} -->
<div class="wp-block-group section-head reveal">
<!-- wp:paragraph {"className":"eyebrow"} -->
<p class="eyebrow">Short label</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2 class="wp-block-heading">The heading of this section</h2>
<!-- /wp:heading -->
<!-- wp:paragraph {"className":"lede"} -->
<p class="lede">An opening sentence that introduces what follows.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
<!-- wp:paragraph -->
<p>The body of the section.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
</section>
<!-- /wp:group -->',
	) );

	register_block_pattern( 'ndop/quote-band', array(
		'title'      => __( 'Quotation band', 'ndop' ),
		'categories' => array( 'ndop' ),
		'content'    => '<!-- wp:group {"tagName":"section","className":"section section--navy"} -->
<section class="wp-block-group section section--navy">
<!-- wp:group {"className":"wrap"} -->
<div class="wp-block-group wrap">
<!-- wp:group {"className":"pullquote reveal"} -->
<div class="wp-block-group pullquote reveal">
<!-- wp:html -->
<div class="rule rule--center" aria-hidden="true"><i></i></div>
<!-- /wp:html -->
<!-- wp:paragraph -->
<p>The sentence worth setting apart from the rest of the page.</p>
<!-- /wp:paragraph -->
<!-- wp:html -->
<cite>Who said it</cite>
<!-- /wp:html -->
</div>
<!-- /wp:group -->
</div>
<!-- /wp:group -->
</section>
<!-- /wp:group -->',
	) );
}
