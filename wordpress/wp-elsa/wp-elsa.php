<?php

/***
 * 
 * CREATE TRANSLATION
 * Receiving new content via POST
 */

add_action('rest_api_init', 'elsa_translation_endpoints');
function elsa_translation_endpoints() {
  register_rest_route(
    'elsa/v1', '/translate/(?P<id>\d+)/(?P<lang>\w+)',
    array(
      'methods' => 'POST',
      'callback' => 'create_translation',
      'args' => array(
        'id' => array(
          'validate_callback' => function($param, $request, $key) {
            return is_numeric( $param );
          }
        ),
        'lang'
      ),
    )
  );
}


/**
 * create_translation
 * 
 * This processes the request from the /translate endpoint and creates
 * a translated content.
 */
function create_translation(WP_REST_Request $request) {
  // Add a custom status code
  $language = $request['lang'];
  $id = $request['id'];

  $current_language = pll_get_post_language($id);

  $json = json_decode($request->get_body());
  $json->id = $id;
  $json->lang = $language;
  
  $new_content = wp_insert_post(
    array(
      'post_title' => $json->title,
      'post_excerpt' => $json->excerpt,
      'post_content' => $json->content
    )
  );


  pll_set_post_language($new_content, $json->lang);

  pll_save_post_translations(array($current_language => $id, $language => $new_content));

  $content = new WP_Query(array('p' => $new_content, 'post_type' => 'any'));

  $response = new WP_REST_Response( 
    $content
  ); 

  $response->set_status(201);
  return $response;
}




/**
 * elsa_requireents_activate
 * 
 * This function would require wordpress to have Polylang installed when acivating the plugin.
 */
function elsa_requirements_activate() {

  if ( current_user_can( 'activate_plugins' ) 
      && !(
        function_exists( 'pll_get_post_language') 
        && function_exists('pll_save_post_translations')
      )
  ) {
    // Deactivate the plugin.
    deactivate_plugins( plugin_basename( __FILE__ ) );
    // Throw an error in the WordPress admin console.
      $error_message = '<p style="font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Oxygen-Sans,Ubuntu,Cantarell,\'Helvetica Neue\',sans-serif;font-size: 13px;line-height: 1.5;color:#444;">' . esc_html__( 'This plugin requires ', 'simplewlv' ) . '<a href="' . esc_url( 'https://wordpress.org/plugins/simplewlv/' ) . '">Polylang</a>' . esc_html__( ' plugin to be active.', 'simplewlv' ) . '</p>';
    die( $error_message ); // WPCS: XSS ok.
  }
}
register_activation_hook( __FILE__, 'elsa_requirements_activate' );
