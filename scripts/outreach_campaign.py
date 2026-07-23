#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import publish_bluesky
import publish_devto
import publish_hashnode
import publish_threads
from publish_utils import dump_json, load_markdown_asset, maybe_write_output, request_json


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAMPAIGN = ROOT / "outreach" / "campaigns" / "japan-sim-guide.json"
LANGUAGE_LABELS = {
    "en": "English",
    "ko": "Korean",
    "zh": "Simplified Chinese",
    "zh-TW": "Traditional Chinese",
    "vi": "Vietnamese",
    "tl": "Filipino",
    "es": "Spanish",
    "id": "Indonesian",
    "ne": "Nepali",
    "pt": "Portuguese",
    "th": "Thai",
}


def load_campaign(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require_key(mapping: dict[str, Any], key: str, label: str) -> Any:
    if key not in mapping:
        raise SystemExit(f"Unknown {label}: {key}")
    return mapping[key]


def platform_mode(campaign: dict[str, Any], platform: str) -> str:
    return require_key(campaign["platforms"], platform, "platform")["mode"]


def normalize_language(campaign: dict[str, Any], landing_language: str) -> str:
    require_key(campaign["landing_languages"], landing_language, "landing language")
    return landing_language


def landing_url(campaign: dict[str, Any], platform: str, landing_language: str, *, methodology: bool = False) -> str:
    base = campaign["base_url"].rstrip("/") + "/"
    lang_path = require_key(campaign["landing_languages"], landing_language, "landing language")
    source_tag = require_key(campaign["platforms"], platform, "platform")["source_tag"]

    if methodology:
        relative = campaign["methodology_path"].lstrip("/")
    else:
        relative = lang_path

    url = base + relative
    if not url.endswith("/"):
        url += "/"
    return f"{url}?src={source_tag}"


def language_hint(landing_language: str) -> str:
    if landing_language == "en":
        return ""
    label = LANGUAGE_LABELS.get(landing_language, landing_language)
    return f"This link opens the {label} version by default.\n\n"


def short_language_hint(landing_language: str) -> str:
    if landing_language == "en":
        return ""
    label = LANGUAGE_LABELS.get(landing_language, landing_language)
    return f"{label} version opens by default."


def angle_summary(campaign: dict[str, Any], angle_id: str) -> dict[str, Any]:
    return require_key(campaign["angles"], angle_id, "angle")


def playbook_definition(campaign: dict[str, Any], playbook_name: str) -> dict[str, Any]:
    return require_key(campaign.get("playbooks", {}), playbook_name, "playbook")


def threads_text(campaign: dict[str, Any], angle_id: str, landing_language: str) -> str:
    angle = angle_summary(campaign, angle_id)
    max_length = require_key(campaign["platforms"], "threads", "platform").get("max_length", 500)
    guide_url = landing_url(campaign, "threads", landing_language)
    disclosure = campaign["disclosure"]["short"] if angle_id == "honest-comparison" else ""
    intro = angle["hook"]
    bullet_lead = "I built a multilingual guide focused on:"
    bullets = angle["bullets"][:]
    outro = angle["cta"]
    hint = language_hint(landing_language).strip()

    def compose(active_bullets: list[str], include_outro: bool, include_hint: bool) -> str:
        lines: list[str] = []
        if disclosure:
            lines.append(disclosure)
            lines.append("")
        lines.append(intro)
        lines.append("")
        lines.append(bullet_lead)
        lines.extend([f"- {bullet}" for bullet in active_bullets])
        if include_hint and hint:
            lines.append("")
            lines.append(hint)
        if include_outro:
            lines.append("")
            lines.append(outro)
        lines.append("")
        lines.append(guide_url)
        return "\n".join(lines).strip()

    active_bullets = bullets[:]
    text = compose(active_bullets, include_outro=True, include_hint=True)
    while len(text) > max_length and active_bullets:
        active_bullets.pop()
        text = compose(active_bullets, include_outro=True, include_hint=True)
    if len(text) > max_length:
        text = compose(active_bullets, include_outro=False, include_hint=True)
    if len(text) > max_length:
        text = compose(active_bullets, include_outro=False, include_hint=False)
    if len(text) > max_length:
        raise SystemExit(f"Threads post for angle {angle_id!r} still exceeds {max_length} characters.")
    return text


def bluesky_text(campaign: dict[str, Any], angle_id: str, landing_language: str) -> str:
    max_length = require_key(campaign["platforms"], "bluesky", "platform").get("max_length", 300)
    disclosure = "I work at Rakuten; the guide clearly labels the referral link."
    hints = [short_language_hint(landing_language)] if landing_language != "en" else []

    hooks = {
        "arrival-friction": "Most Japan SIM advice assumes you're already settled.",
        "honest-comparison": "Most Japan SIM posts hide the real tradeoffs for foreigners.",
        "multilingual-helper": "Japan SIM advice gets messy fast when someone has to translate it.",
    }
    focus_lines = {
        "arrival-friction": "I built a guide for week-one issues: eSIM on arrival, no Japanese credit card yet, and document friction.",
        "honest-comparison": "I compared Rakuten vs docomo / au / SoftBank on real monthly cost, signup friction, and when Rakuten is not the best fit.",
        "multilingual-helper": "It keeps the same comparison, checklist, and calculator across 11 languages for newcomers and the people helping them.",
    }
    require_key(hooks, angle_id, "angle")
    require_key(focus_lines, angle_id, "angle")

    def compose(include_hint: bool) -> str:
        parts = [
            disclosure,
            hooks[angle_id],
            focus_lines[angle_id],
        ]
        if include_hint and hints:
            parts.append(hints[0])
        return "\n\n".join(parts).strip()

    text = compose(include_hint=True)
    if len(text) > max_length:
        text = compose(include_hint=False)
    if len(text) > max_length:
        raise SystemExit(f"Bluesky post for angle {angle_id!r} still exceeds {max_length} characters.")
    return text


def bluesky_card(campaign: dict[str, Any], landing_language: str) -> dict[str, str]:
    card = require_key(campaign.get("link_cards", {}), "bluesky", "link card")
    return {
        "url": landing_url(campaign, "bluesky", landing_language),
        "title": card["title"],
        "description": card["description"],
    }


def reddit_title(campaign: dict[str, Any], angle_id: str) -> str:
    if angle_id == "arrival-friction":
        return "I made a multilingual Japan SIM guide for foreigners (calculator + signup checklist)"
    if angle_id == "honest-comparison":
        return "I built an honest Rakuten vs docomo / au / SoftBank guide for foreigners moving to Japan"
    if angle_id == "multilingual-helper":
        return "I built an 11-language Japan SIM guide for newcomers and the people helping them"
    return f"{campaign['name']} outreach draft"


def reddit_body(campaign: dict[str, Any], angle_id: str, landing_language: str) -> str:
    angle = angle_summary(campaign, angle_id)
    guide_url = landing_url(campaign, "reddit", landing_language)
    methodology_url = landing_url(campaign, "reddit", landing_language, methodology=True)
    hint = language_hint(landing_language)
    points = campaign["proof_points"][:4]
    lines = [
        campaign["disclosure"]["medium"],
        "",
        angle["hook"],
        "",
        angle["problem"],
        "",
        "I made the guide around the parts new residents actually get stuck on:",
    ]
    lines.extend([f"- {bullet}" for bullet in angle["bullets"]])
    lines.append("")
    lines.append("The guide includes:")
    lines.extend([f"- {point}" for point in points])
    lines.append("")
    if hint:
        lines.append(hint.strip())
        lines.append("")
    lines.append("Main guide:")
    lines.append(guide_url)
    lines.append("")
    lines.append("Methodology / disclosure page:")
    lines.append(methodology_url)
    lines.append("")
    lines.append("If anything looks misleading, outdated, or too biased, I would genuinely appreciate the feedback and will fix it.")
    return "\n".join(lines)


def reddit_render(campaign: dict[str, Any], angle_id: str, landing_language: str) -> str:
    subreddit = campaign["manual_targets"]["reddit_subreddit"]
    return "\n".join(
        [
            f"# Reddit draft for {subreddit}",
            "",
            "## Suggested title",
            "",
            reddit_title(campaign, angle_id),
            "",
            "## Suggested body",
            "",
            reddit_body(campaign, angle_id, landing_language),
        ]
    )


def quora_render(campaign: dict[str, Any], angle_id: str, landing_language: str) -> str:
    angle = angle_summary(campaign, angle_id)
    guide_url = landing_url(campaign, "quora", landing_language)
    methodology_url = landing_url(campaign, "quora", landing_language, methodology=True)
    question = campaign["manual_targets"]["quora_question_seed"]
    hint = language_hint(landing_language)
    lines = [
        "Question idea:",
        question,
        "",
        "Answer draft:",
        "",
        angle["hook"],
        "",
        angle["problem"],
        "",
        "If I were helping a newcomer decide, I would compare these first:",
        "1. Can they sign up without a Japanese credit card yet?",
        "2. Is eSIM available immediately?",
        "3. Is the signup and support flow realistic in English?",
        "4. Are the required documents straightforward for a new resident?",
        "",
        "That lens often points people toward Rakuten Mobile, especially when they have just arrived and want the least friction.",
        "",
        "The guide I built includes:",
    ]
    lines.extend([f"- {point}" for point in campaign["proof_points"][:5]])
    if hint:
        lines.extend(["", hint.strip()])
    lines.extend(
        [
            "",
            "Guide:",
            guide_url,
            "",
            "Methodology:",
            methodology_url,
            "",
            campaign["disclosure"]["long"],
        ]
    )
    return "\n".join(lines)


def threads_render(campaign: dict[str, Any], angle_id: str, landing_language: str) -> str:
    return threads_text(campaign, angle_id, landing_language)


def bluesky_render(campaign: dict[str, Any], angle_id: str, landing_language: str) -> str:
    return bluesky_text(campaign, angle_id, landing_language)


def render_content(campaign: dict[str, Any], platform: str, angle_id: str | None, landing_language: str) -> str:
    if platform == "threads":
        if not angle_id:
            raise SystemExit("--angle is required for threads.")
        return threads_render(campaign, angle_id, landing_language)
    if platform == "bluesky":
        if not angle_id:
            raise SystemExit("--angle is required for bluesky.")
        return bluesky_render(campaign, angle_id, landing_language)
    if platform == "reddit":
        if not angle_id:
            raise SystemExit("--angle is required for reddit.")
        return reddit_render(campaign, angle_id, landing_language)
    if platform == "quora":
        if not angle_id:
            raise SystemExit("--angle is required for quora.")
        return quora_render(campaign, angle_id, landing_language)
    raise SystemExit(f"Platform {platform!r} does not render manual copy.")


def filename_for(platform: str, angle_id: str, landing_language: str) -> str:
    extension = "txt" if platform in {"threads", "bluesky"} else "md"
    return f"{platform}-{landing_language}-{angle_id}.{extension}"


def planned_filename(task: dict[str, Any]) -> str:
    platform = task["platform"]
    landing_language = task.get("landing_language", "en")
    angle_id = task.get("angle")
    if platform in {"reddit", "quora", "threads", "bluesky"} and angle_id:
        return filename_for(platform, angle_id, landing_language)
    if platform == "devto":
        return f"devto-{landing_language}-draft.json"
    if platform == "hashnode":
        return f"hashnode-{landing_language}-draft.json"
    return f"{platform}-{landing_language}.json"


def task_command(task: dict[str, Any], output_dir: str | None = None) -> str:
    platform = task["platform"]
    landing_language = task.get("landing_language", "en")
    angle_id = task.get("angle")
    target_arg = f" --output-dir {output_dir}" if output_dir and platform in {"reddit", "quora"} else ""
    output_arg = ""
    if output_dir and platform in {"threads", "bluesky", "devto", "hashnode"}:
        output_arg = f" --output {Path(output_dir) / planned_filename(task)}"

    if platform in {"reddit", "quora"}:
        return (
            f"python3 scripts/outreach_campaign.py dispatch --platform {platform} "
            f"--angle {angle_id} --landing-language {landing_language}{target_arg}"
        )
    if platform == "threads":
        return (
            "THREADS_ACCESS_TOKEN=... "
            f"python3 scripts/outreach_campaign.py dispatch --platform threads "
            f"--angle {angle_id} --landing-language {landing_language}{output_arg}"
        )
    if platform == "bluesky":
        return (
            "BLUESKY_HANDLE=... BLUESKY_APP_PASSWORD=... "
            f"python3 scripts/outreach_campaign.py dispatch --platform bluesky "
            f"--angle {angle_id} --landing-language {landing_language}{output_arg}"
        )
    if platform == "devto":
        return (
            "DEVTO_API_KEY=... "
            f"python3 scripts/outreach_campaign.py dispatch --platform devto{output_arg}"
        )
    if platform == "hashnode":
        return (
            "HASHNODE_PAT=... HASHNODE_PUBLICATION_ID=... "
            f"python3 scripts/outreach_campaign.py dispatch --platform hashnode{output_arg}"
        )
    return f"# Unsupported platform: {platform}"


def list_summary(campaign: dict[str, Any]) -> str:
    lines = ["Platforms:"]
    for platform, settings in campaign["platforms"].items():
        lines.append(f"- {platform}: {settings['mode']}")
    lines.append("")
    lines.append("Angles:")
    for angle_id, angle in campaign["angles"].items():
        lines.append(f"- {angle_id}: {angle['label']}")
    lines.append("")
    lines.append("Landing languages:")
    lines.append("- " + ", ".join(campaign["landing_languages"].keys()))
    return "\n".join(lines)


def validate_campaign(campaign: dict[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {
        "campaign": campaign["id"],
        "threads_checks": [],
        "bluesky_checks": [],
        "playbook_checks": [],
        "status": "ok",
    }

    for angle_id in campaign["angles"].keys():
        for landing_language in campaign["landing_languages"].keys():
            text = threads_text(campaign, angle_id, landing_language)
            results["threads_checks"].append(
                {
                    "angle": angle_id,
                    "landing_language": landing_language,
                    "length": len(text),
                    "status": "ok",
                }
            )
            bluesky = bluesky_text(campaign, angle_id, landing_language)
            results["bluesky_checks"].append(
                {
                    "angle": angle_id,
                    "landing_language": landing_language,
                    "length": publish_bluesky.count_text_length(bluesky),
                    "status": "ok",
                }
            )

    for playbook_name, definition in campaign.get("playbooks", {}).items():
        for idx, task in enumerate(definition.get("tasks", []), start=1):
            platform = require_key(campaign["platforms"], task["platform"], "platform")
            landing_language = normalize_language(campaign, task.get("landing_language", "en"))
            if task["platform"] in {"threads", "bluesky", "reddit", "quora"}:
                angle_id = task.get("angle")
                if not angle_id:
                    raise SystemExit(f"Playbook {playbook_name} task {idx} is missing an angle.")
                angle_summary(campaign, angle_id)
            results["playbook_checks"].append(
                {
                    "playbook": playbook_name,
                    "task": idx,
                    "platform": task["platform"],
                    "mode": platform["mode"],
                    "landing_language": landing_language,
                    "status": "ok",
                }
            )

    return results


def append_list_section(lines: list[str], title: str, items: list[str] | None) -> None:
    if not items:
        return
    lines.append(f"## {title}")
    lines.append("")
    for item in items:
        lines.append(f"- {item}")
    lines.append("")


def export_bundle(
    campaign: dict[str, Any],
    *,
    output_dir: Path,
    landing_language: str,
    platforms: list[str],
    angles: list[str],
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {"campaign": campaign["id"], "landing_language": landing_language, "assets": []}

    for platform in platforms:
        mode = platform_mode(campaign, platform)
        if platform in {"threads", "bluesky", "reddit", "quora"}:
            for angle_id in angles:
                content = render_content(campaign, platform, angle_id, landing_language)
                path = output_dir / filename_for(platform, angle_id, landing_language)
                path.write_text(content + "\n", encoding="utf-8")
                manifest["assets"].append(
                    {
                        "platform": platform,
                        "mode": mode,
                        "angle": angle_id,
                        "path": str(path),
                    }
                )
            continue

        manifest["assets"].append(
            {
                "platform": platform,
                "mode": mode,
                "article_file": str(ROOT / campaign["article_file"]),
            }
        )

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(dump_json(manifest) + "\n", encoding="utf-8")
    manifest["manifest_path"] = str(manifest_path)
    return manifest


def render_playbook_markdown(campaign: dict[str, Any], playbook_name: str, *, output_dir: str | None = None) -> str:
    definition = playbook_definition(campaign, playbook_name)
    lines = [f"# Playbook: {playbook_name}", "", definition["summary"], ""]

    goal = definition.get("goal")
    if goal:
        lines.extend(["## Goal", "", goal, ""])

    append_list_section(lines, "Prerequisites", definition.get("prerequisites"))
    append_list_section(lines, "Rules", definition.get("rules"))

    review_window = definition.get("review_window")
    review_prompt = definition.get("review_prompt")
    if review_window or review_prompt:
        lines.append("## Review")
        lines.append("")
        if review_window:
            lines.append(f"- Window: {review_window}")
        if review_prompt:
            lines.append(f"- Prompt: {review_prompt}")
        lines.append("")

    for idx, task in enumerate(definition.get("tasks", []), start=1):
        platform = task["platform"]
        landing_language = task.get("landing_language", "en")
        angle_id = task.get("angle")
        lines.append(f"## {idx}. {platform}")
        lines.append("")
        lines.append(f"- Action: {task['action']}")
        if window := task.get("window"):
            lines.append(f"- Window: {window}")
        lines.append(f"- Landing language: {landing_language}")
        if angle_id:
            lines.append(f"- Angle: {angle_id}")
        lines.append(f"- Note: {task['note']}")
        lines.append(f"- Command: `{task_command(task, output_dir)}`")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def prepare_playbook_assets(campaign: dict[str, Any], playbook_name: str, output_dir: Path) -> dict[str, Any]:
    definition = playbook_definition(campaign, playbook_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "campaign": campaign["id"],
        "playbook": playbook_name,
        "summary": definition["summary"],
        "tasks": [],
    }
    if goal := definition.get("goal"):
        manifest["goal"] = goal
    if prerequisites := definition.get("prerequisites"):
        manifest["prerequisites"] = prerequisites
    if rules := definition.get("rules"):
        manifest["rules"] = rules
    if review_window := definition.get("review_window"):
        manifest["review_window"] = review_window
    if review_prompt := definition.get("review_prompt"):
        manifest["review_prompt"] = review_prompt

    queue_path = output_dir / "PLAYBOOK.md"
    queue_path.write_text(render_playbook_markdown(campaign, playbook_name, output_dir=str(output_dir)), encoding="utf-8")
    manifest["playbook_path"] = str(queue_path)

    for idx, task in enumerate(definition.get("tasks", []), start=1):
        platform = task["platform"]
        landing_language = task.get("landing_language", "en")
        angle_id = task.get("angle")
        output_path = output_dir / planned_filename(task)
        metadata: dict[str, Any] = {
            "task": idx,
            "platform": platform,
            "action": task["action"],
            "landing_language": landing_language,
            "note": task["note"],
            "command": task_command(task, str(output_dir)),
            "path": str(output_path),
        }
        if angle_id:
            metadata["angle"] = angle_id
        if window := task.get("window"):
            metadata["window"] = window

        if platform in {"reddit", "quora"}:
            content = render_content(campaign, platform, angle_id, landing_language)
            output_path.write_text(content + "\n", encoding="utf-8")
        elif platform == "threads":
            content = publish_threads_dispatch(
                campaign,
                SimpleNamespace(
                    angle=angle_id,
                    landing_language=landing_language,
                    dry_run=True,
                    access_token=None,
                ),
            )
            output_path.write_text(content + "\n", encoding="utf-8")
        elif platform == "bluesky":
            content = publish_bluesky_dispatch(
                campaign,
                SimpleNamespace(
                    angle=angle_id,
                    landing_language=landing_language,
                    dry_run=True,
                    identifier=None,
                    app_password=None,
                    service=None,
                    pds_host=None,
                ),
            )
            output_path.write_text(content + "\n", encoding="utf-8")
        elif platform == "devto":
            content = publish_devto_dispatch(
                campaign,
                SimpleNamespace(
                    api_key=None,
                    publish=False,
                    dry_run=True,
                ),
            )
            output_path.write_text(content + "\n", encoding="utf-8")
        elif platform == "hashnode":
            content = publish_hashnode_dispatch(
                campaign,
                SimpleNamespace(
                    api_key=None,
                    publication_id="your_publication_id",
                    publish=False,
                    dry_run=True,
                ),
            )
            output_path.write_text(content + "\n", encoding="utf-8")
        else:
            raise SystemExit(f"Unsupported playbook platform: {platform}")

        manifest["tasks"].append(metadata)

    manifest_path = output_dir / "playbook-manifest.json"
    manifest_path.write_text(dump_json(manifest) + "\n", encoding="utf-8")
    manifest["manifest_path"] = str(manifest_path)
    return manifest


def publish_threads_dispatch(campaign: dict[str, Any], args: argparse.Namespace) -> str:
    text = threads_text(campaign, args.angle, args.landing_language)
    thread_args = SimpleNamespace(
        reply_control=None,
        reply_to_id=None,
        link_attachment=None,
        topic_tag=None,
        location_id=None,
        enable_reply_approvals=False,
        ghost_post=False,
        alt_text=None,
        auto_publish_text=False,
        image_url=None,
        video_url=None,
        create_only=False,
        no_lookup=False,
        lookup_fields=publish_threads.DEFAULT_LOOKUP_FIELDS,
    )
    query = publish_threads.build_container_query(thread_args, text, "TEXT")

    if args.dry_run:
        return publish_threads.render_dry_run(
            text=text,
            text_source={"type": "campaign", "angle": args.angle, "landing_language": args.landing_language},
            media_type="TEXT",
            create_query=query,
            create_only=False,
            auto_publish_text=False,
        )

    access_token = args.access_token or os.environ.get("THREADS_ACCESS_TOKEN")
    if not access_token:
        raise SystemExit("Missing Threads access token. Set THREADS_ACCESS_TOKEN or pass --access-token.")

    container = publish_threads.create_container(access_token, query)
    creation_id = container.get("id")
    if not creation_id:
        raise SystemExit("Meta did not return a Threads creation container ID.")
    published = publish_threads.publish_container(access_token, str(creation_id))
    payload: dict[str, Any] = {
        "platform": "threads",
        "angle": args.angle,
        "landing_language": args.landing_language,
        "text": text,
        "container": container,
        "published": published,
    }
    post_id = published.get("id")
    if post_id:
        payload["details"] = publish_threads.lookup_post(access_token, str(post_id), publish_threads.DEFAULT_LOOKUP_FIELDS)
    return dump_json(payload)


def publish_bluesky_dispatch(campaign: dict[str, Any], args: argparse.Namespace) -> str:
    text = bluesky_text(campaign, args.angle, args.landing_language)
    max_length = require_key(campaign["platforms"], "bluesky", "platform").get("max_length", publish_bluesky.DEFAULT_MAX_LENGTH)
    card = bluesky_card(campaign, args.landing_language)
    record = publish_bluesky.build_post_record(
        text,
        langs=["en"],
        add_link_facets=True,
        external_url=card["url"],
        external_title=card["title"],
        external_description=card["description"],
    )

    service = (args.service or os.environ.get("BLUESKY_SERVICE") or publish_bluesky.DEFAULT_SERVICE).rstrip("/")
    pds_host = args.pds_host or os.environ.get("BLUESKY_PDS_HOST")

    if args.dry_run:
        return publish_bluesky.render_dry_run(
            text=text,
            text_source={"type": "campaign", "angle": args.angle, "landing_language": args.landing_language},
            record=record,
            identifier=args.identifier or os.environ.get("BLUESKY_HANDLE"),
            service=service,
            pds_host=pds_host,
            max_length=max_length,
        )

    identifier = args.identifier or os.environ.get("BLUESKY_HANDLE")
    app_password = args.app_password or os.environ.get("BLUESKY_APP_PASSWORD")
    if not identifier:
        raise SystemExit("Missing Bluesky identifier. Set BLUESKY_HANDLE or pass --identifier.")
    if not app_password:
        raise SystemExit("Missing Bluesky App Password. Set BLUESKY_APP_PASSWORD or pass --app-password.")

    session = publish_bluesky.create_session(identifier, app_password, service=service)
    resolved_pds = publish_bluesky.resolve_pds_host(session, service=service, explicit_pds_host=pds_host)
    created = publish_bluesky.create_post(
        access_token=str(session["accessJwt"]),
        pds_host=resolved_pds,
        repo=str(session.get("did") or identifier),
        record=record,
    )

    payload: dict[str, Any] = {
        "platform": "bluesky",
        "angle": args.angle,
        "landing_language": args.landing_language,
        "text": text,
        "text_length": publish_bluesky.count_text_length(text),
        "record": record,
        "session": {
            "handle": session.get("handle"),
            "did": session.get("did"),
            "pds_host": resolved_pds,
        },
        "created": created,
    }
    public_url = publish_bluesky.public_post_url(
        str(session.get("handle") or session.get("did") or ""),
        str(created.get("uri") or ""),
    )
    if public_url:
        payload["public_url"] = public_url
    return dump_json(payload)


def publish_devto_dispatch(campaign: dict[str, Any], args: argparse.Namespace) -> str:
    api_key = args.api_key or os.environ.get("DEVTO_API_KEY")
    article_path = ROOT / campaign["article_file"]
    metadata, body = load_markdown_asset(article_path)
    payload = publish_devto.build_payload(
        metadata,
        body,
        SimpleNamespace(
            title=None,
            description=None,
            canonical_url=None,
            main_image=None,
            series=None,
            slug=None,
            tags=None,
            organization_id=None,
            publish=bool(args.publish),
        ),
    )

    if args.dry_run:
        return dump_json(
            {
                "platform": "devto",
                "article_file": str(article_path),
                "publish": bool(args.publish),
                "payload": payload,
            }
        )

    if not api_key:
        raise SystemExit("Missing dev.to API key. Set DEVTO_API_KEY or pass --api-key.")

    response = request_json(
        url=publish_devto.DEVTO_URL,
        headers={
            "accept": "application/vnd.forem.api-v1+json",
            "content-type": "application/json",
            "api-key": api_key,
        },
        payload=payload,
    )
    return dump_json(response)


def publish_hashnode_dispatch(campaign: dict[str, Any], args: argparse.Namespace) -> str:
    api_key = args.api_key or os.environ.get("HASHNODE_PAT")
    publication_id = args.publication_id or os.environ.get("HASHNODE_PUBLICATION_ID")
    article_path = ROOT / campaign["article_file"]
    metadata, body = load_markdown_asset(article_path)
    post_input = publish_hashnode.build_input(
        metadata,
        body,
        SimpleNamespace(
            publication_id=publication_id,
            subtitle=None,
            slug=None,
            canonical_url=None,
            cover_image=None,
            tags=None,
            publish_as=None,
            series_id=None,
            title=None,
        ),
    )
    operation = publish_hashnode.build_operation(post_input, publish=bool(args.publish))

    if args.dry_run:
        return dump_json(
            {
                "platform": "hashnode",
                "article_file": str(article_path),
                "publish": bool(args.publish),
                "operation": operation,
            }
        )

    if not api_key:
        raise SystemExit("Missing Hashnode PAT. Set HASHNODE_PAT or pass --api-key.")
    if not publication_id:
        raise SystemExit("Missing Hashnode publication ID. Set HASHNODE_PUBLICATION_ID or pass --publication-id.")

    response = request_json(
        url=publish_hashnode.HASHNODE_URL,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
        },
        payload=operation,
    )
    return dump_json(response)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Central outreach runner for Japan SIM Guide distribution channels.")
    parser.add_argument("--campaign-file", default=str(DEFAULT_CAMPAIGN), help="Campaign JSON file.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="Show platforms, angles, and landing languages.")
    list_parser.add_argument("--output", help="Optional file path for the rendered output.")

    validate_parser = subparsers.add_parser("validate", help="Validate all Threads and Bluesky variants plus playbook references.")
    validate_parser.add_argument("--output", help="Optional file path for the rendered JSON.")

    render_parser = subparsers.add_parser("render", help="Render one platform-specific asset.")
    render_parser.add_argument("--platform", required=True, choices=["threads", "bluesky", "reddit", "quora"])
    render_parser.add_argument("--angle", required=True)
    render_parser.add_argument("--landing-language", default="en")
    render_parser.add_argument("--output", help="Optional file path for the rendered asset.")

    bundle_parser = subparsers.add_parser("bundle", help="Render a batch of platform assets into a directory.")
    bundle_parser.add_argument("--landing-language", default="en")
    bundle_parser.add_argument("--platforms", default="threads,bluesky,reddit,quora,devto,hashnode", help="Comma-separated platform list.")
    bundle_parser.add_argument("--angles", default="all", help="Comma-separated angles or 'all'.")
    bundle_parser.add_argument("--output-dir", required=True, help="Directory for rendered assets.")
    bundle_parser.add_argument("--output", help="Optional file path for the manifest JSON.")

    playbook_parser = subparsers.add_parser("playbook", help="Show or materialize a recommended execution playbook.")
    playbook_parser.add_argument("--name", default="launch", help="Playbook name from the campaign JSON.")
    playbook_parser.add_argument("--output-dir", help="If set, write task assets and a queue file into this directory.")
    playbook_parser.add_argument("--output", help="Optional file path for the rendered output or manifest JSON.")

    dispatch_parser = subparsers.add_parser("dispatch", help="Publish to an API-backed platform or export a manual draft.")
    dispatch_parser.add_argument("--platform", required=True, choices=["threads", "bluesky", "reddit", "quora", "devto", "hashnode"])
    dispatch_parser.add_argument("--angle", help="Required for threads/bluesky/reddit/quora.")
    dispatch_parser.add_argument("--landing-language", default="en")
    dispatch_parser.add_argument("--output", help="Optional file path for the rendered output.")
    dispatch_parser.add_argument("--output-dir", help="Directory used when exporting a manual draft.")
    dispatch_parser.add_argument("--dry-run", action="store_true", help="Render payloads without sending them.")
    dispatch_parser.add_argument("--publish", action="store_true", help="Publish immediately on dev.to or Hashnode instead of creating a draft.")
    dispatch_parser.add_argument("--access-token", help="Threads access token override.")
    dispatch_parser.add_argument("--identifier", help="Bluesky handle or DID override.")
    dispatch_parser.add_argument("--app-password", help="Bluesky App Password override.")
    dispatch_parser.add_argument("--service", help="Bluesky login host or entryway override.")
    dispatch_parser.add_argument("--pds-host", help="Optional direct Bluesky PDS host override.")
    dispatch_parser.add_argument("--api-key", help="dev.to API key or Hashnode PAT, depending on platform.")
    dispatch_parser.add_argument("--publication-id", help="Hashnode publication ID.")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    campaign = load_campaign(args.campaign_file)

    if args.command == "list":
        rendered = list_summary(campaign)
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    if args.command == "validate":
        rendered = dump_json(validate_campaign(campaign))
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    if args.command == "render":
        landing_language = normalize_language(campaign, args.landing_language)
        rendered = render_content(campaign, args.platform, args.angle, landing_language)
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    if args.command == "bundle":
        landing_language = normalize_language(campaign, args.landing_language)
        platforms = [item.strip() for item in args.platforms.split(",") if item.strip()]
        for platform in platforms:
            require_key(campaign["platforms"], platform, "platform")
        if args.angles == "all":
            angles = list(campaign["angles"].keys())
        else:
            angles = [item.strip() for item in args.angles.split(",") if item.strip()]
            for angle_id in angles:
                require_key(campaign["angles"], angle_id, "angle")

        manifest = export_bundle(
            campaign,
            output_dir=Path(args.output_dir),
            landing_language=landing_language,
            platforms=platforms,
            angles=angles,
        )
        rendered = dump_json(manifest)
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    if args.command == "playbook":
        if args.output_dir:
            manifest = prepare_playbook_assets(campaign, args.name, Path(args.output_dir))
            rendered = dump_json(manifest)
            print(rendered)
            maybe_write_output(args.output, rendered)
            return
        rendered = render_playbook_markdown(campaign, args.name)
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    if args.command == "dispatch":
        platform = args.platform
        landing_language = normalize_language(campaign, args.landing_language)

        if platform in {"reddit", "quora"}:
            if not args.angle:
                raise SystemExit("--angle is required for reddit and quora.")
            rendered = render_content(campaign, platform, args.angle, landing_language)
            if args.output_dir:
                output_dir = Path(args.output_dir)
                output_dir.mkdir(parents=True, exist_ok=True)
                target = output_dir / filename_for(platform, args.angle, landing_language)
                target.write_text(rendered + "\n", encoding="utf-8")
                payload = {
                    "platform": platform,
                    "mode": "manual-export",
                    "path": str(target),
                    "angle": args.angle,
                    "landing_language": landing_language,
                }
                rendered_json = dump_json(payload)
                print(rendered_json)
                maybe_write_output(args.output, rendered_json)
                return
            print(rendered)
            maybe_write_output(args.output, rendered)
            return

        if platform == "threads":
            if not args.angle:
                raise SystemExit("--angle is required for threads.")
            rendered = publish_threads_dispatch(campaign, args)
            print(rendered)
            maybe_write_output(args.output, rendered)
            return

        if platform == "bluesky":
            if not args.angle:
                raise SystemExit("--angle is required for bluesky.")
            rendered = publish_bluesky_dispatch(campaign, args)
            print(rendered)
            maybe_write_output(args.output, rendered)
            return

        if platform == "devto":
            rendered = publish_devto_dispatch(campaign, args)
            print(rendered)
            maybe_write_output(args.output, rendered)
            return

        if platform == "hashnode":
            rendered = publish_hashnode_dispatch(campaign, args)
            print(rendered)
            maybe_write_output(args.output, rendered)
            return

        raise SystemExit(f"Unsupported platform: {platform}")


if __name__ == "__main__":
    main()
