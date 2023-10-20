---
title: "Send chatMessage in a channel or a chat"
description: "Send a new chatMessage in the specified channel or a chat."
ms.localizationpriority: medium
author: "RamjotSingh"
ms.prod: "microsoft-teams"
doc_type: apiPageType
---

# Send chatMessage in a channel or a chat

Namespace: microsoft.graph

Send a new [chatMessage](../resources/chatmessage.md) in the specified [channel](../resources/channel.md) or a [chat](../resources/chat.md).

> **Note**: We don't recommend that you use this API for data migration. It does not have the throughput necessary for a typical migration.

> **Note**: It is a violation of the [terms of use](/legal/microsoft-apis/terms-of-use) to use Microsoft Teams as a log file. Only send messages that people will read.

## Permissions

One of the following permissions is required to call this API. To learn more, including how to choose permissions, see [Permissions](/graph/permissions-reference).

### Permissions for channel
| Permission type                        | Permissions (from least to most privileged) |
|:---------------------------------------|:--------------------------------------------|
| Delegated (work or school account)     | ChannelMessage.Send, Group.ReadWrite.All** |
| Delegated (personal Microsoft account) | Not supported. |
| Application                            | Teamwork.Migrate.All |

> **Note**: Permissions marked with ** are supported only for backward compatibility. We recommend that you update your solutions to use an alternative permission listed in the previous table and avoid using these permissions going forward.

> **Note**: Application permissions are *only* supported for [migration](/microsoftteams/platform/graph-api/import-messages/import-external-messages-to-teams). In the future, Microsoft may require you or your customers to pay additional fees based on the amount of data imported.

### Permissions for chat
| Permission type                        | Permissions (from least to most privileged) |
|:---------------------------------------|:--------------------------------------------|
| Delegated (work or school account)     | ChatMessage.Send, Chat.ReadWrite |
| Delegated (personal Microsoft account) | Not supported. |
| Application                            | Not supported. |

## HTTP request

**Sending message in a channel**
<!-- { "blockType": "ignored" } -->
```http
POST /teams/{team-id}/channels/{channel-id}/messages
```

**Sending replies in a channel**
<!-- { "blockType": "ignored" } -->
```http
POST /teams/{team-id}/channels/{channel-id}/messages/{message-id}/replies
```

**Sending message in a chat**
<!-- { "blockType": "ignored" } -->
```http
POST /chats/{chat-id}/messages
```

## Request headers

| Name          | Description   |
|:--------------|:--------------|
| Authorization | Bearer {code}. Required. |
| Content-type | application/json. Required. |

## Request body

In the request body, supply a JSON representation of a [chatMessage](../resources/chatmessage.md) object. Only the body property is mandatory; other properties are optional.


## Response

If successful, this method returns a `201 Created` response code and a new [chatMessage](../resources/chatmessage.md) object in the response body.

## Examples

In the following examples, the URL can use the [HTTP syntax](#http-request) described to [send a message to a chat](chat-post-messages.md), [send a message to a channel](channel-post-messages.md), or [send reply to a channel](chatmessage-post-replies.md).


```http
POST https://graph.microsoft.com/v1.0/chats/{chatId}/messages

Request Body: 
Content-type: application/json

{
  "body": {
    "content": "Hello World"
  }
}
```

# [C#](#tab/csharp)
[!INCLUDE [sample-code](../includes/snippets/csharp/post-chatmessage-11-csharp-snippets.md)]
[!INCLUDE [sdk-documentation](../includes/snippets/snippets-sdk-documentation-link.md)]

# [CLI](#tab/cli)
[!INCLUDE [sample-code](../includes/snippets/cli/post-chatmessage-11-cli-snippets.md)]
[!INCLUDE [sdk-documentation](../includes/snippets/snippets-sdk-documentation-link.md)]

# [Go](#tab/go)
[!INCLUDE [sample-code](../includes/snippets/go/post-chatmessage-11-go-snippets.md)]
[!INCLUDE [sdk-documentation](../includes/snippets/snippets-sdk-documentation-link.md)]

# [Java](#tab/java)
[!INCLUDE [sample-code](../includes/snippets/java/post-chatmessage-11-java-snippets.md)]
[!INCLUDE [sdk-documentation](../includes/snippets/snippets-sdk-documentation-link.md)]

# [JavaScript](#tab/javascript)
[!INCLUDE [sample-code](../includes/snippets/javascript/post-chatmessage-11-javascript-snippets.md)]
[!INCLUDE [sdk-documentation](../includes/snippets/snippets-sdk-documentation-link.md)]

# [PHP](#tab/php)
[!INCLUDE [sample-code](../includes/snippets/php/post-chatmessage-11-php-snippets.md)]
[!INCLUDE [sdk-documentation](../includes/snippets/snippets-sdk-documentation-link.md)]

# [PowerShell](#tab/powershell)
[!INCLUDE [sample-code](../includes/snippets/powershell/post-chatmessage-11-powershell-snippets.md)]
[!INCLUDE [sdk-documentation](../includes/snippets/snippets-sdk-documentation-link.md)]

# [Python](#tab/python)
[!INCLUDE [sample-code](../includes/snippets/python/post-chatmessage-11-python-snippets.md)]
[!INCLUDE [sdk-documentation](../includes/snippets/snippets-sdk-documentation-link.md)]

---

---