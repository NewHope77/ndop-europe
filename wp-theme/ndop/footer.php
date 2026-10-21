<?php
/**
 * Closing of every page: the verse, the two link columns, and the viewer that
 * enlarges any image marked data-lightbox.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand footer-brand" href="<?php echo esc_url( home_url( '/' ) ); ?>">
          <svg class="brand__mark" viewBox="0 0 40 40" fill="none" aria-hidden="true">
            <circle cx="20" cy="20" r="19" stroke="#ffffff" stroke-width="1.4" opacity=".65"/>
            <path d="M20 8v24M12.5 15.5h15" stroke="#3BA6D8" stroke-width="2" stroke-linecap="round"/>
            <circle cx="20" cy="20" r="6.4" stroke="#ffffff" stroke-width="1.1" opacity=".3"/>
          </svg>
          <span class="brand__text">
            <span class="brand__name">National Days of Prayer</span>
            <span class="brand__sub">Movement in Europe</span>
          </span>
        </a>
        <p class="footer-verse">
          <?php echo esc_html( ndop_option( 'footer_verse' ) ); ?>
          <cite><?php echo esc_html( ndop_option( 'footer_verse_cite' ) ); ?></cite>
        </p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul class="footer-links">
          <li><a href="<?php echo esc_url( ndop_page_url( 'about' ) ); ?>">About Us</a></li>
          <li><a href="<?php echo esc_url( ndop_page_url( 'history' ) ); ?>">History</a></li>
          <li><a href="<?php echo esc_url( ndop_page_url( 'resources' ) ); ?>">Resources &amp; Legal Base</a></li>
          <li><a href="<?php echo esc_url( ndop_page_url( 'faq' ) ); ?>">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul class="footer-links">
          <li><a href="<?php echo esc_url( ndop_page_url( 'about' ) . '#board' ); ?>">International Board</a></li>
          <li><a href="mailto:<?php echo esc_attr( ndop_email() ); ?>"><?php echo esc_html( ndop_email() ); ?></a></li>
          <li><a href="<?php echo esc_url( get_theme_file_uri( 'assets/docs/ndop-in-europe-brochure.pdf' ) ); ?>" download>Download the brochure (PDF)</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year"><?php echo esc_html( gmdate( 'Y' ) ); ?></span> The National Days of Prayer Movement in Europe</span>
      <span><?php echo esc_html( ndop_option( 'footer_tagline' ) ); ?></span>
    </div>
  </div>
</footer>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer">
  <button class="lightbox__close" id="lightboxClose" aria-label="Close">
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M4 4l12 12M16 4L4 16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
  </button>
  <figure style="margin:0;text-align:center">
    <img id="lightboxImg" alt="" hidden>
    <figcaption id="lightboxCap"></figcaption>
  </figure>
</div>

<?php wp_footer(); ?>
</body>
</html>
