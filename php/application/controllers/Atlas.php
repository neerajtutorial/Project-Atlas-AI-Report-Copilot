<?php
defined('BASEPATH') OR exit('No direct script access allowed');
class Atlas extends CI_Controller {
  public function __construct(){ parent::__construct(); $this->load->library('atlas_api'); $this->load->database(); }
  public function index(){ $this->load->view('atlas_chat'); }
  public function ask(){
    if ($this->input->method(TRUE) !== 'POST') show_error('Method not allowed',405);
    $client = trim((string)$this->input->post('client_id',TRUE)); $question = trim((string)$this->input->post('question',TRUE));
    if (!preg_match('/^C-[0-9]{2}$/',$client) || strlen($question)<3 || strlen($question)>4000) { $this->output->set_status_header(422)->set_content_type('application/json')->set_output(json_encode(['error'=>'Invalid client or question'])); return; }
    $result = $this->atlas_api->chat($client,$question);
    $this->db->insert('conversations',['client_id'=>$client,'question'=>$question,'answer'=>$result['answer']??($result['error']??'Service unavailable'),'response_json'=>json_encode($result)]);
    $this->output->set_content_type('application/json')->set_output(json_encode($result));
  }
  public function feedback(){ $id=(int)$this->input->post('conversation_id'); $rating=$this->input->post('rating',TRUE); if($id<1 || !in_array($rating,['up','down'],TRUE)){ show_error('Invalid feedback',422); return; } $this->db->insert('feedback',['conversation_id'=>$id,'rating'=>$rating,'comment'=>$this->input->post('comment',TRUE)]); $this->output->set_content_type('application/json')->set_output(json_encode(['status'=>'saved'])); }
}