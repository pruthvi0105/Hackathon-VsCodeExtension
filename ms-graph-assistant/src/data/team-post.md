---
title: "Create team"
description: "Create a new team."
author: "anandjo"
ms.localizationpriority: high
ms.prod: "microsoft-teams"
doc_type: apiPageType
---

BaseURL: https://graph.microsoft.com/v1.0

# Create team

Namespace: microsoft.graph

[!INCLUDE [beta-disclaimer](../../includes/beta-disclaimer.md)]

Create a new [team](../resources/team.md).

## Permissions

One of the following permissions is required to call this API. To learn more, including how to choose permissions, see [Permissions](/graph/permissions-reference).

| Permission type                        | Permissions (from least to most privileged) |
| :------------------------------------- | :------------------------------------------ |
| Delegated (work or school account)     | Team.Create, Group.ReadWrite.All**, Directory.ReadWrite.All** |
| Delegated (personal Microsoft account) | Not supported.                              |
| Application                            | Team.Create, Teamwork.Migrate.All, Group.ReadWrite.All**, Directory.ReadWrite.All** |

> **Note**: The Teamwork.Migrate.All permission is *only* supported for [migration](/microsoftteams/platform/graph-api/import-messages/import-external-messages-to-teams).
In the future, Microsoft may require you or your customers to pay additional fees based on the amount of data imported.

> **Note**: Permissions marked with ** are supported only for backward compatibility. We recommend that you update your solutions to use an alternative permission listed in the previous table and avoid using these permissions going forward.

## HTTP request

<!-- { "blockType": "ignored" } -->

```http
POST /teams
```

## Request headers

| Header        | Value                     |
| :------------ | :------------------------ |
| Authorization | Bearer {token}. Required. |
| Content-Type  | application/json. Required. |

## Request body

In the request body, supply a JSON representation of a [team](../resources/team.md) object.

## Response

If successful, this API returns a `202 Accepted` response that contains a link to the [teamsAsyncOperation](../resources/teamsasyncoperation.md).

## Examples

### Example 1: Delegated permissions

The following is an example of a minimal request. By omitting other properties, the client is implicitly taking defaults from the pre-defined template represented by `template`.

#### Request

# [HTTP](#tab/http)
<!-- {
  "blockType": "request",
  "name": "create_team_post_e1"
}-->
```http
POST https://graph.microsoft.com/beta/teams
Content-Type: application/json

{
  "template@odata.bind": "https://graph.microsoft.com/beta/teamsTemplates('standard')",
  "displayName": "My Sample Team",
  "description": "My Sample Team’s Description"
}
```