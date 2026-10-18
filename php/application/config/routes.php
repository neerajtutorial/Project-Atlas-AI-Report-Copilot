<?php
defined('BASEPATH') OR exit('No direct script access allowed');
$route['default_controller'] = 'atlas';
$route['atlas/ask']['post'] = 'atlas/ask';
$route['atlas/feedback']['post'] = 'atlas/feedback';
$route['404_override'] = '';
$route['translate_uri_dashes'] = FALSE;