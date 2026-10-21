<?php
/**
 * The masthead: brand, primary navigation, theme switch.
 *
 * Kept as a template rather than a block pattern on purpose. It carries the
 * movement's emblem, the sun/moon switch and the burger, all of which the
 * script addresses by id — expressed as blocks they would be easy for an
 * editor to break and hard to repair.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?> data-page="<?php echo esc_attr( ndop_current_page_slug() ); ?>">
<?php wp_body_open(); ?>
<a class="skip" href="#main">Skip to content</a>

<header class="site-header" id="siteHeader">
  <div class="wrap site-header__inner">
    <a class="brand" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="The National Days of Prayer Movement in Europe — home">
      <svg class="brand__mark" viewBox="0 0 40 40" fill="none" aria-hidden="true">
        <circle cx="20" cy="20" r="19" stroke="#0C335B" stroke-width="1.4"/>
        <path d="M20 8v24M12.5 15.5h15" stroke="#0389C3" stroke-width="2" stroke-linecap="round"/>
        <circle cx="20" cy="20" r="6.4" stroke="#0C335B" stroke-width="1.1" opacity=".45"/>
      </svg>
      <span class="brand__text">
        <span class="brand__name">National Days of Prayer</span>
        <span class="brand__sub">Movement in Europe</span>
      </span>
    </a>

    <nav class="nav" id="primaryNav" aria-label="Primary">
      <?php
      foreach ( ndop_nav_items() as $slug => $label ) {
          printf(
              '<a href="%s" data-nav="%s">%s</a>',
              esc_url( ndop_page_url( $slug ) ),
              esc_attr( $slug ),
              esc_html( $label )
          );
      }
      ?>
      <a class="btn btn--primary header-cta" href="<?php echo esc_url( ndop_page_url( 'contact' ) . '#join' ); ?>">Join the Movement</a>
    </nav>

    <div class="header-actions">
      <button class="theme-toggle" id="themeToggle" type="button" aria-pressed="false" aria-label="Switch to dark theme" title="Switch theme">
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="12" cy="12" r="4.4" stroke="currentColor" stroke-width="1.6"/>
          <path d="M12 2.4v2.4M12 19.2v2.4M2.4 12h2.4M19.2 12h2.4M5.2 5.2l1.7 1.7M17.1 17.1l1.7 1.7M18.8 5.2l-1.7 1.7M6.9 17.1l-1.7 1.7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
        </svg>
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M20.5 14.2A8.6 8.6 0 019.8 3.5a8.6 8.6 0 1010.7 10.7z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>
        </svg>
      </button>

      <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="primaryNav" aria-label="Toggle navigation">
        <span></span>
      </button>
    </div>
  </div>
</header>

<main id="main">
