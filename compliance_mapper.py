import argparse
import subprocess
from core.collector import run_collector
from core.ontology import print_summary, build_master_control_ontology, auto_generate_control_json, save_generated_controls
from core.mapper import run_phase3_mapper
from core.reporter import summarize_coverage, group_matches_by_control, generate_report_file
from core.watcher import start_watchdog
import yaml
import os

def run_phase1():
    print("Running Phase 1: Input Collector")
    run_collector()

def run_phase2():
    print("Running Phase 2: Ontology Summary")
    print_summary()

def run_phase3():
    print("Running Phase 3: AI Compliance Mapper")
    run_phase3_mapper()

def run_phase4():
    print("Running Phase 4: Gap Reporter")
    with open("data/parsed/phase3_matches.yaml", "r", encoding="utf-8") as f:
        matches = yaml.safe_load(f)
    ontology = build_master_control_ontology()
    summary = summarize_coverage(matches, ontology)
    grouped = group_matches_by_control(matches)
    generate_report_file(summary, grouped, ontology)

def run_phase5():
    print("Running Phase 5: Continuous Watchdog")
    start_watchdog()

def run_generate_controls():
    print("Generating Ontologies from Raw Control Text")
    frameworks = {
        "nis2": ("docs/raw_controls/raw_nis2.txt", "controls/nis2.json"),
        "dora": ("docs/raw_controls/raw_dora.txt", "controls/dora.json"),
        "iso27001": ("docs/raw_controls/raw_iso27001.txt", "controls/iso27001.json"),
    }
    for prefix, (infile, outfile) in frameworks.items():
        with open(infile, "r", encoding="utf-8") as f:
            raw_text = f.read()
        print(f"Generating controls for {prefix.upper()}...")
        controls = auto_generate_control_json(raw_text, prefix.upper())
        save_generated_controls(controls, outfile)

def run_all_phases():
    run_generate_controls()
    run_phase1()
    run_phase2()
    run_phase3()
    run_phase4()
    run_phase5()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NIS2-DORA-ISO27001 Compliance Mapper Engine")
    parser.add_argument("--full", action="store_true", help="Run all phases end-to-end")
    parser.add_argument("--phase1", action="store_true", help="Run input collector")
    parser.add_argument("--phase2", action="store_true", help="Run ontology summary")
    parser.add_argument("--phase3", action="store_true", help="Run AI compliance matcher")
    parser.add_argument("--phase4", action="store_true", help="Run gap report generator")
    parser.add_argument("--phase5", action="store_true", help="Run continuous assurance engine")
    parser.add_argument("--generate-controls", action="store_true", help="Generate controls from raw regulatory text")

    args = parser.parse_args()

    if args.full:
        run_all_phases()
    if args.generate_controls:
        run_generate_controls()
    if args.phase1:
        run_phase1()
    if args.phase2:
        run_phase2()
    if args.phase3:
        run_phase3()
    if args.phase4:
        run_phase4()
    if args.phase5:
        run_phase5()
