create database driver_sentiment;
use driver_sentiment;
create table drivers(id int primary key auto_increment, name varchar(100), total_feedbacks int, cumulative_score float, average_score float, last_alert datetime);
create table feedback(id int primary key auto_increment, driver_id int, feedback_text text, sentiment_score float, created_at datetime default current_timestamp);