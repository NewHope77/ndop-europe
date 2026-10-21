<?php
/**
 * The handful of strings that live outside any page: the footer verse and the
 * line beneath it.
 *
 * They belong to the footer, which is a template, so there is no block for the
 * client to click. The Customizer gives them one screen with a live preview
 * and nothing else to break.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Defaults, taken from the brochure. */
function ndop_option_defaults() {
	return array(
		'footer_verse'      => '“… if my people, who are called by my name, humble themselves and pray, and seek my face, and turn from their wicked ways, then I will hear from heaven and forgive their sin, and heal their land.”',
		'footer_verse_cite' => 'Bible, 2 Chronicles 7:14',
		'footer_tagline'    => 'Uniting Europe in prayer for its nations, freedom and peace.',
	);
}

/** One of those strings, falling back to the brochure's wording. */
function ndop_option( $key ) {
	$defaults = ndop_option_defaults();
	$default  = isset( $defaults[ $key ] ) ? $defaults[ $key ] : '';
	return get_theme_mod( 'ndop_' . $key, $default );
}

add_action( 'customize_register', 'ndop_customize' );
function ndop_customize( $wp_customize ) {
	$wp_customize->add_section( 'ndop_footer', array(
		'title'       => __( 'Footer', 'ndop' ),
		'priority'    => 30,
		'description' => __( 'The verse and the line that close every page.', 'ndop' ),
	) );

	$fields = array(
		'footer_verse'      => array( __( 'Verse', 'ndop' ), 'textarea' ),
		'footer_verse_cite' => array( __( 'Reference', 'ndop' ), 'text' ),
		'footer_tagline'    => array( __( 'Closing line', 'ndop' ), 'text' ),
	);

	$defaults = ndop_option_defaults();

	foreach ( $fields as $key => $field ) {
		list( $label, $type ) = $field;

		$wp_customize->add_setting( 'ndop_' . $key, array(
			'default'           => $defaults[ $key ],
			'sanitize_callback' => 'wp_kses_post',
			'transport'         => 'refresh',
		) );

		$wp_customize->add_control( 'ndop_' . $key, array(
			'section' => 'ndop_footer',
			'label'   => $label,
			'type'    => $type,
		) );
	}
}
