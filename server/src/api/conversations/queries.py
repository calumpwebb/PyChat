from sqlalchemy import text

from src import config


def get_conversations_ids_and_last_messages(requesting_user_id):
    # gets all the conversations ids and the final message they sent

    query = """
        WITH

        _conversation_ids AS (
            SELECT
                DISTINCT(id)
            FROM
                conversations
            WHERE
                user_id_1 = :requesting_user_id OR user_id_2 = :requesting_user_id 
        ),

        _last_messages AS (
            SELECT
                DISTINCT ON (M.conversation_id)
                M.message as last_message,
                M.conversation_id,
                M.sent_datetime,
                M.from_user_id = :requesting_user_id  as own_message,
                CASE
                    WHEN M.to_user_id = :requesting_user_id  THEN M.from_user_id
                    WHEN M.from_user_id = :requesting_user_id  THEN M.to_user_id
                END as user_id
            FROM
                messages M
            WHERE
                M.conversation_id IN (SELECT id FROM _conversation_ids)
            ORDER BY
                M.conversation_id, M.sent_datetime DESC
        )

        SELECT
            json_build_object(
                'sent_datetime', LM.sent_datetime,
                'conversation_id', LM.conversation_id,
                'own_message', LM.own_message,
                'user_id', LM.user_id,
                'username', U.username,
                'last_message', LM.last_message
            ) as messages
        FROM
            _last_messages LM
        LEFT JOIN 
            users U ON (
                U.id = LM.user_id
            )
        ORDER BY
            LM.sent_datetime DESC 

    """

    session = config.get_session()

    last_messages = session.execute(
        text(query).params(requesting_user_id=requesting_user_id)
    ).fetchall()

    return {
        'conversations': [mess[0] for mess in last_messages]
    }


def get_conversation_messages(conversation_id, limit=100):
    query = """
        SELECT
            json_build_object(
                'message_id', M.id,
                'sent_datetime', M.sent_datetime,
                'from_user_id', M.from_user_id,
                'from_username', Uf.username,
                'to_user_id', M.to_user_id,
                'to_username', Ut.username,
                'message', M.message 
            ) as messages
        FROM
            messages M
        LEFT JOIN users Ut ON (
            M.to_user_id = Ut.id
        )
        LEFT JOIN users Uf ON (
            M.from_user_id = Uf.id
        )
        WHERE
            M.conversation_id = :conversation_id
        ORDER BY
            sent_datetime
        LIMIT :limit
    """
    session = config.get_session()

    messages = session.execute(
        text(query).params(conversation_id=conversation_id, limit=limit)
    ).fetchall()

    return {"messages": [mes[0] for mes in messages]}
