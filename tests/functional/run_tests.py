#!/usr/bin/env python3

import json
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "http://localhost:9345"

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
SERVER_BIN = PROJECT_ROOT / "target" / "debug" / "simeis-server"


def api_call(method: str, path: str, key: str | None = None) -> dict:
    url = BASE_URL + path
    req = urllib.request.Request(url, method=method)

    if key is not None:
        req.add_header("Simeis-Key", key)

    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")

    data = json.loads(body)
    return data


def check_ok(data: dict, context: str = "") -> dict:
    if data.get("error") != "ok":
        msg = data.get("error", "erreur inconnue")
        etype = data.get("type", "")
        raise AssertionError(
            f"[{context}] Erreur API inattendue : {msg} (type={etype}) | réponse complète : {data}"
        )
    return data


def print_step(msg: str) -> None:
    print(f"  --> {msg}")


def print_ok(msg: str) -> None:
    print(f"  [OK] {msg}")


def start_server() -> subprocess.Popen:
    print(f"Démarrage du serveur : {SERVER_BIN}")

    if not SERVER_BIN.exists():
        raise FileNotFoundError(
            f"Binaire introuvable : {SERVER_BIN}\n"
            "Compilez le serveur avec : cargo build --features testing"
        )

    proc = subprocess.Popen(
        [str(SERVER_BIN)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=str(PROJECT_ROOT),
    )

    deadline = time.time() + 15.0
    while time.time() < deadline:
        try:
            data = api_call("GET", "/ping")
            if data.get("ping") == "pong":
                print("Serveur prêt.\n")
                return proc
        except Exception:
            pass
        time.sleep(0.2)

    proc.kill()
    raise RuntimeError("Le serveur n'a pas démarré dans les 15 secondes.")


def stop_server(proc: subprocess.Popen) -> None:
    print("\nArrêt du serveur...")
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
    print("Serveur arrêté.")


def main() -> int:
    server_proc = None
    try:
        server_proc = start_server()
    except (FileNotFoundError, RuntimeError) as e:
        print(f"ERREUR : Impossible de démarrer le serveur : {e}", file=sys.stderr)
        return 1

    erreur = None
    try:
        print("=== Tous les tests fonctionnels ont réussi ! ===")
    except AssertionError as e:
        print(f"\nECHEC : Assertion non vérifiée : {e}", file=sys.stderr)
        erreur = e
    except Exception as e:
        print(
            f"\nECHEC : Erreur inattendue : {type(e).__name__} : {e}", file=sys.stderr
        )
        erreur = e
    finally:
        if server_proc is not None:
            stop_server(server_proc)

    return 0 if erreur is None else 1


if __name__ == "__main__":
    sys.exit(main())
