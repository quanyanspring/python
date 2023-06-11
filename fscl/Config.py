insert_resource_sql = """
               INSERT INTO t_resource_inf (title, resource_url, resource_url_type, invite_time, content, resource_type, name, area,
                            is_delete, source_type, create_time, update_time)
                VALUES ({0}, {1}, 0, null, null, 3, {2}, null, 0, 0,NOW(6), NOW(6));
            """

update_article_sql = """
              update t_article_inf set cover_resource_id = {0} where id = {1};
            """

select_article_sql = """
                select t.source_id, tt.id as resourceId, tt.resource_url, t.id as articleId
                from t_article_inf t
                         left join t_resource_inf tt on t.cover_resource_id = tt.id
                where t.article_type = 5
                  and t.source_id > {0}
                order by t.source_id asc;
            """