-- TODO: permission system
CREATE TABLE users (
  user_id             bigserial     primary key,
  user_name           varchar(32)   not null,
  user_email          varchar(254)  unique not null,
  user_password_hash  varchar(60)   not null,
  user_timestamp      timestamp     not null,
  user_avatar         varchar(32)   not null -- md5 hash of email for gravatar
);

CREATE TABLE channels (
  chan_id         bigserial     primary key,
  chan_name       varchar(50)   not null,
  chan_desc       varchar(512),
  chan_timestamp  timestamp     not null
);

CREATE TABLE messages (
  msg_id        bigserial     primary key,
  author_id     bigint        references users(user_id),
  chan_id       bigint        references channels(chan_id),
  msg_content   varchar(2000) not null,
  msg_timestamp timestamp     not null
);
