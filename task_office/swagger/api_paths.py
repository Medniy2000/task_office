API_PATHS = {
    # Auth
    "/api/v1/auth/sign-up": {
        "post": {
            "tags": ["Auth"],
            "summary": "Sign Up, Create new User",
            "requestBody": {
                "description": "Sign Up Post Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/UserSignUpSchema"}
                    }
                },
            },
            "produces": ["application/json"],
            "responses": {
                "201": {
                    "required": True,
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/UserSchema"},
                },
                "400": {"description": "Failed. Bad post data."},
                "422": {"description": "Failed. Bad post data."},
            },
        }
    },
    "/api/v1/auth/sign-in": {
        "post": {
            "tags": ["Auth"],
            "summary": "Sign In User",
            "requestBody": {
                "description": "Sign In Post Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/UserSignInSchema"}
                    }
                },
            },
            "produces": ["application/json"],
            "responses": {
                "201": {
                    "required": True,
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/SignedSchema"},
                },
                "400": {"description": "Failed. Bad post data."},
                "422": {"description": "Failed. Bad post data."},
            },
        }
    },
    "/api/v1/auth/refresh": {
        "post": {
            "tags": ["Auth"],
            "summary": "Refresh Access token",
            "requestBody": {
                "description": "Refresh Post Object",
                "required": True,
                "content": {"application/json": {}},
            },
            "produces": ["application/json"],
            "responses": {
                "200": {
                    "required": True,
                    "description": "OK",
                    "schema": {
                        "$ref": "#/components/schemas/RefreshedAccessTokenSchema"
                    },
                },
                "400": {"description": "Failed. Bad post data."},
                "401": {"description": "Failed. Bad post data."},
                "422": {"description": "Failed. Bad post data."},
            },
        }
    },
    # Boards
    "/api/v1/boards": {
        "post": {
            "tags": ["Boards"],
            "summary": "Boards create",
            "requestBody": {
                "description": "Boards Post Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/BoardActionsSchema"}
                    }
                },
            },
            "produces": ["application/json"],
            "responses": {
                "200": {
                    "required": True,
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/BoardDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        },
        "get": {
            "tags": ["Boards"],
            "summary": "Returns Boards",
            "requestBody": {
                "description": "Boards get Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/BoardListQuerySchema"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/BoardDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        },
    },
    "/api/v1/boards/<board_uuid>": {
        "get": {
            "tags": ["Boards"],
            "summary": "Returns Boards",
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/BoardDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "404": {"description": "Failed. Not found."},
                "422": {"description": "Failed. Bad data."},
            },
        },
        "put": {
            "tags": ["Boards"],
            "summary": "Boards update",
            "requestBody": {
                "description": "Boards Put Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/BoardActionsSchema"}
                    }
                },
            },
            "produces": ["application/json"],
            "responses": {
                "200": {
                    "required": True,
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/BoardDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        },
    },
    "/api/v1/boards/<board_uuid>/users": {
        "get": {
            "tags": ["Boards"],
            "summary": "Returns Users of boards",
            "requestBody": {
                "description": "Users get Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/UserListByBoardQuerySchema"
                        }
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/NestedUserDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "404": {"description": "Failed. Not found."},
                "422": {"description": "Failed. Bad data."},
            },
        }
    },
    "/api/v1/boards/<board_uuid>/columns": {
        "post": {
            "tags": ["Columns"],
            "summary": "Boards Columns create",
            "requestBody": {
                "description": "Boards Columns Post Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ColumnPostSchema"}
                    }
                },
            },
            "produces": ["application/json"],
            "responses": {
                "200": {
                    "required": True,
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/ColumnDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "404": {"description": "Failed. Not found."},
                "422": {"description": "Failed. Bad data."},
            },
        },
        "get": {
            "tags": ["Columns"],
            "summary": "Returns Boards Columns",
            "requestBody": {
                "description": "Boards Columns Get Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ColumnListQuerySchema"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/ColumnDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "404": {"description": "Failed. Not found."},
                "422": {"description": "Failed. Bad data."},
            },
        },
    },
    "/api/v1/boards/<board_uuid>/columns/<column_uuid>": {
        "put": {
            "tags": ["Columns"],
            "summary": "Boards Columns Update",
            "requestBody": {
                "description": "Update Boards Columns Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ColumnPutSchema"}
                    }
                },
            },
            "produces": ["application/json"],
            "responses": {
                "200": {
                    "required": True,
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/ColumnDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "404": {"description": "Failed. Not found."},
                "422": {"description": "Failed. Bad data."},
            },
        }
    },
    # Tasks
    "/api/v1/boards/<board_uuid>/tasks": {
        "post": {
            "tags": ["Tasks"],
            "summary": "Tasks create",
            "requestBody": {
                "description": "Tasks Post Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/TaskPostSchema"}
                    }
                },
            },
            "produces": ["application/json"],
            "responses": {
                "200": {
                    "required": True,
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/TaskDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        },
        "get": {
            "tags": ["Tasks"],
            "summary": "Returns Tasks",
            "requestBody": {
                "description": "Tasks Get list of Objects",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/TaskListQuerySchema"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/TaskDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        },
    },
    "/api/v1/boards/<board_uuid>/tasks/<task_uuid>": {
        "put": {
            "tags": ["Tasks"],
            "summary": "Tasks Update",
            "requestBody": {
                "description": "Tasks Put Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/TaskPutSchema"}
                    }
                },
            },
            "produces": ["application/json"],
            "responses": {
                "200": {
                    "required": True,
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/TaskDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        }
    },
    "/api/v1/boards/<board_uuid>/tasks/by-columns": {
        "get": {
            "tags": ["Tasks"],
            "summary": "Returns Tasks",
            "requestBody": {
                "description": "Tasks by columns Get list of Objects",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/TaskListByColumnsQuerySchema"
                        }
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/TaskDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        }
    },
    "/api/v1/boards/<board_uuid>/tasks/meta": {
        "get": {
            "tags": ["Tasks"],
            "summary": "Returns additional tasks info",
            "responses": {
                "200": {"description": "OK", "schema": {}},
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        }
    },
    # Permissions
    "/api/v1/boards/<board_uuid>/permissions": {
        "post": {
            "tags": ["Permissions"],
            "summary": "Permissions create",
            "requestBody": {
                "description": "Permissions Post Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/PermissionQuerySchema"}
                    }
                },
            },
            "produces": ["application/json"],
            "responses": {
                "200": {
                    "required": True,
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/ PermissionDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        },
        "get": {
            "tags": ["Permissions"],
            "summary": "Returns Permissions",
            "requestBody": {
                "description": "Permissions get list of Objects",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "#/components/schemas/PermissionListQuerySchema"
                        }
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/PermissionDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        },
    },
    "/api/v1/boards/<board_uuid>/permissions/<permission_uuid>": {
        "put": {
            "tags": ["Permissions"],
            "summary": "Permissions update",
            "requestBody": {
                "description": "Permissions Put Object",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/PermissionQuerySchema"}
                    }
                },
            },
            "produces": ["application/json"],
            "responses": {
                "200": {
                    "required": True,
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/ PermissionDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        },
        "get": {
            "tags": ["Permissions"],
            "summary": "Returns Permissions",
            "responses": {
                "200": {
                    "description": "OK",
                    "schema": {"$ref": "#/components/schemas/PermissionDumpSchema"},
                },
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        },
    },
    "/api/v1/boards/<board_uuid>/permissions/meta": {
        "get": {
            "tags": ["Permissions"],
            "summary": "Returns additions permissions info",
            "responses": {
                "200": {"description": "OK", "schema": {}},
                "400": {"description": "Failed. Bad data."},
                "401": {"description": "Failed. Not authorized."},
                "403": {"description": "Failed. Not denied."},
                "422": {"description": "Failed. Bad data."},
            },
        }
    },
}
