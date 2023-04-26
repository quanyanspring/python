queryListPage_sql = """
        select
            tga.id,
            tga.request_id as requestId,
            tga.activity_no as activityNo,
            tga.parent_activity_no as parentActivityNo,
            tga.activity_title as activityTitle,
            tga.activity_type as activityType,
            tga.activity_sub_type as activitySubType,
            tga.business_type,
            tgad.apply_amount as applyAmount,
            tga.apply_person_ad as applyPersonAd,
            tga.apply_person_name as applyPersonName,
            tga.activity_status as activityStatus,
            tga.grant_method as grantMethod,
            tga.receiver_identity as receiverIdentity,
            tga.grant_acc_no as grantAccNo,
            tgad.fk_preuse_id as fkPreuseId,
            DATE_FORMAT(tga.create_time,'%Y-%m-%d %H:%i:%S') as createTime,
            DATE_FORMAT(tga.modify_time,'%Y-%m-%d %H:%i:%S') as modifyTime,
            tgad.apply_status as applyStatus,
            tgad.bpm_instance_id as instanceId,
            tga.logic_flag as logicFlag,
            tga.temp_json
        from t_platform_grant_activity tga
        left join t_platform_grant_activity_detail tgad on tga.request_id = tgad.request_id
        where tga.is_deleted = 0 and ((tga.logic_flag=0 and tga.activity_status!=3) or tga.logic_flag=1)
            and tga.auth_parent_activity_no is null and tgad.apply_status in (1,3) and tga.create_time > '2022-01-01 00:00:00' and tga.create_time < '2022-12-31 00:00:00' order by SUBSTR(tga.activity_no,3,17) desc,tga.id asc
 """

listSumGrantAmt_sql = """
    SELECT
            RTRIM(activity_no) as activityNo,
            sum( CASE WHEN grant_status = 1 and grant_type = 1 THEN grant_amount ELSE 0 END ) doneGrantSum,
            sum( CASE WHEN grant_status = 2 and grant_type = 1 THEN grant_amount ELSE 0 END ) failGrantSum,
            sum( CASE WHEN grant_status = 4 and grant_type = 1 THEN grant_amount ELSE 0 END ) frozenGrantSum,
            sum( CASE WHEN grant_status = 1 and grant_type = 2 THEN refunded_amount ELSE 0 END) refundedAmountSum,
            sum( CASE WHEN grant_status = 5 and grant_type = 1 THEN grant_amount ELSE 0 END ) unRegistExpiresGrantSum
        FROM
            t_platform_grant_list
        WHERE
            is_deleted = 0
        GROUP BY
            activity_no
"""