# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import runpy
from pathlib import Path


def test_lillio_production_config_uses_separate_async_redis_databases(
    monkeypatch,
) -> None:
    monkeypatch.setenv("REDIS_HOST", "cache.example")
    monkeypatch.setenv("REDIS_PASSWORD", "secret")
    monkeypatch.setenv("GLOBAL_ASYNC_QUERIES_JWT_SECRET", "jwt-secret")
    monkeypatch.setenv("SMTP_USER", "smtp-user")
    monkeypatch.setenv("SMTP_PASSWORD", "smtp-password")
    config = runpy.run_path(
        str(Path(__file__).parents[3] / "docker/lillio/superset_config.py")
    )

    assert config["CELERY_CONFIG"].broker_url.endswith("/1?ssl_cert_reqs=required")
    assert config["CELERY_CONFIG"].result_backend.endswith("/2?ssl_cert_reqs=required")
    assert (
        config["RESULTS_BACKEND"]._write_client.connection_pool.connection_kwargs["db"]
        == 3
    )
    assert config["GLOBAL_ASYNC_QUERIES_CACHE_BACKEND"]["CACHE_REDIS_DB"] == 5
    assert "/6?ssl_cert_reqs=required" in config["DATA_CACHE_CONFIG"]["CACHE_REDIS_URL"]


def test_lillio_production_config_enforces_embedding_and_security(monkeypatch) -> None:
    monkeypatch.setenv("REDIS_HOST", "cache.example")
    monkeypatch.setenv("REDIS_PASSWORD", "secret")
    monkeypatch.setenv("GLOBAL_ASYNC_QUERIES_JWT_SECRET", "jwt-secret")
    monkeypatch.setenv("SMTP_USER", "smtp-user")
    monkeypatch.setenv("SMTP_PASSWORD", "smtp-password")
    config = runpy.run_path(
        str(Path(__file__).parents[3] / "docker/lillio/superset_config.py")
    )

    assert config["FEATURE_FLAGS"]["EMBEDDED_SUPERSET"] is True
    assert config["FEATURE_FLAGS"]["SQLLAB_FORCE_RUN_ASYNC"] is True
    assert config["SESSION_SERVER_SIDE"] is True
    assert config["SESSION_COOKIE_SAMESITE"] == "None"
    assert config["TALISMAN_CONFIG"]["content_security_policy"]["frame-ancestors"] == [
        "'self'",
        "https://app.lillio.com",
        "https://staging-app.lillio.com",
        "https://*.herokuapp.com",
    ]
