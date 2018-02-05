drop table if exists entries;
create table entries (
  'key' text primary key,
  'parent' text not null,
  'pos' text,
  'text' text
);