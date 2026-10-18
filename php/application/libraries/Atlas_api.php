<?php
defined('BASEPATH') OR exit('No direct script access allowed');
class Atlas_api {
  private $url; private $key;
  public function __construct(){ $this->url=getenv('ATLAS_API_URL') ?: 'http://api:8000'; $this->key=getenv('ATLAS_API_KEY') ?: 'local-dev-key-change-me'; }
  public function chat($client_id,$question){ $body=json_encode(['client_id'=>$client_id,'question'=>$question]); $ch=curl_init($this->url.'/chat'); curl_setopt_array($ch,[CURLOPT_POST=>TRUE,CURLOPT_POSTFIELDS=>$body,CURLOPT_HTTPHEADER=>['Content-Type: application/json','X-API-Key: '.$this->key],CURLOPT_RETURNTRANSFER=>TRUE,CURLOPT_CONNECTTIMEOUT=>3,CURLOPT_TIMEOUT=>25]); $raw=curl_exec($ch); $status=curl_getinfo($ch,CURLINFO_HTTP_CODE); curl_close($ch); if($raw===FALSE || $status>=500) return ['answer'=>'The report assistant is temporarily unavailable. Please try again or contact an analyst.','citations'=>[],'confidence'=>0,'conflicts'=>[],'derived_values'=>[],'escalated'=>TRUE]; $data=json_decode($raw,TRUE); return is_array($data)?$data:['answer'=>'The assistant returned an invalid response. Please contact an analyst.','escalated'=>TRUE]; }
}