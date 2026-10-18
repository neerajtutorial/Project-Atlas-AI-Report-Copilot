CREATE TABLE IF NOT EXISTS reports (
  id VARCHAR(20) PRIMARY KEY, title VARCHAR(255) NOT NULL, publisher VARCHAR(100) NOT NULL,
  published DATE, sector VARCHAR(100), access_type VARCHAR(30) NOT NULL DEFAULT 'paid',
  description TEXT
);
CREATE TABLE IF NOT EXISTS market_metrics (
  id INT AUTO_INCREMENT PRIMARY KEY, report_id VARCHAR(20) NOT NULL, metric VARCHAR(100) NOT NULL,
  region VARCHAR(100), period VARCHAR(30), value_num DECIMAL(14,4), unit VARCHAR(40), scope_note TEXT,
  FOREIGN KEY (report_id) REFERENCES reports(id)
);
CREATE TABLE IF NOT EXISTS clients (
  id VARCHAR(20) PRIMARY KEY, company VARCHAR(255) NOT NULL, contact_email VARCHAR(255),
  purchased_reports JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS chunks (
  id VARCHAR(64) PRIMARY KEY, report_id VARCHAR(20) NOT NULL, sector VARCHAR(100), region VARCHAR(100),
  year INT, page_num INT, text MEDIUMTEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (report_id) REFERENCES reports(id)
);
CREATE TABLE IF NOT EXISTS conversations (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, client_id VARCHAR(20) NOT NULL, question TEXT NOT NULL,
  answer MEDIUMTEXT, response_json JSON, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS feedback (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, conversation_id BIGINT NOT NULL, rating ENUM('up','down') NOT NULL,
  comment TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
CREATE TABLE IF NOT EXISTS escalations (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, client_id VARCHAR(20) NOT NULL, question TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL, status ENUM('open','in_progress','closed') DEFAULT 'open',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS security_events (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, client_id VARCHAR(20), event_type VARCHAR(80) NOT NULL,
  details TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS request_logs (
  id BIGINT AUTO_INCREMENT PRIMARY KEY, client_id VARCHAR(20), latency_ms INT, estimated_cost_usd DECIMAL(10,6) DEFAULT 0,
  cached BOOLEAN DEFAULT FALSE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT IGNORE INTO reports VALUES
('R-101','Global Smart Water Meter Market 2025','CMR','2025-03-10','Utilities','paid','Global market including hardware, software and services.'),
('R-102','Smart Water Metering: Industry Outlook 2024','Aquila Insights','2024-06-18','Utilities','public excerpt','Hardware-only AMR/AMI scope; public excerpt.'),
('R-103','Residential Water Purifier Market 2025','CMR','2025-01-22','Consumer Durables','paid','Residential water purifier market.'),
('R-104','APAC Solar Inverter Market 2025','CMR','2025-02-05','Energy','paid','Synthetic demonstration report.'),
('R-105','Global Industrial IoT Sensors 2025','CMR','2025-02-14','Industrial Technology','paid','Synthetic demonstration report.'),
('R-106','India Electric Two-Wheeler Outlook 2025','CMR','2025-03-01','Automotive','paid','Synthetic demonstration report.'),
('R-107','Global Cold Chain Logistics 2025','CMR','2025-03-07','Logistics','paid','Synthetic demonstration report.');
INSERT IGNORE INTO market_metrics (report_id,metric,region,period,value_num,unit,scope_note) VALUES
('R-101','Market size','Global','2024',4.21,'USD billion','Includes hardware, software and services'),
('R-101','CAGR','Global','2025-2030',11.2,'percent','Forecast period stated as 2025-2030'),
('R-101','Regional share','APAC','2024',38,'percent','Share of global market size'),
('R-102','Market size','Global','2024',3.87,'USD billion','AMR / AMI hardware only'),
('R-102','CAGR','Global','2024-2029',9.8,'percent','Different forecast window from R-101'),
('R-102','Regional share','APAC','2024',41,'percent','Share of hardware market');
INSERT IGNORE INTO clients VALUES
('C-01','Northwind Utilities','ops@example.com',JSON_ARRAY('R-101','R-103','R-104','R-105','R-106','R-107')),
('C-02','Blue Delta Infra','procurement@example.com',JSON_ARRAY('R-103'));