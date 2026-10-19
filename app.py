
import streamlit as st
import pandas as pd
from pathlib import Path

# Interceptor ScaleReady
# Initial research prototype — not affiliated with The Ocean Cleanup.

st.set_page_config(
    page_title="Interceptor ScaleReady",
    page_icon="🌊",
    layout="wide",
)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
REGISTER_FILE = DATA_DIR / "research_register.csv"

UNDP_URL = (
    "https://www.undp.org/vietnam/publications/"
    "towards-sustainable-financial-model-floating-waste-management-"
    "waterways-lessons-interceptor-003-model-can-tho-viet-nam"
)

STARTER_DATA = [
    {
        "ID": "R001",
        "Category": "Operations",
        "Research question": "Who operates Interceptor 003?",
        "Finding": "",
        "Source URL": UNDP_URL,
        "Evidence status": "To investigate",
        "Product implication": "",
    },
    {
        "ID": "R002",
        "Category": "Maintenance",
        "Research question": "What maintenance arrangements are documented?",
        "Finding": "",
        "Source URL": UNDP_URL,
        "Evidence status": "To investigate",
        "Product implication": "",
    },
    {
        "ID": "R003",
        "Category": "Waste management",
        "Research question": "How is collected waste transported and handled?",
        "Finding": "",
        "Source URL": UNDP_URL,
        "Evidence status": "To investigate",
        "Product implication": "",
    },
    {
        "ID": "R004",
        "Category": "Funding",
        "Research question": "What is documented about long-term operating costs?",
        "Finding": "",
        "Source URL": UNDP_URL,
        "Evidence status": "To investigate",
        "Product implication": "",
    },
    {
        "ID": "R005",
        "Category": "Handover",
        "Research question": "What responsibilities do local partners assume?",
        "Finding": "",
        "Source URL": UNDP_URL,
        "Evidence status": "To investigate",
        "Product implication": "",
    },
]

if not REGISTER_FILE.exists():
    pd.DataFrame(STARTER_DATA).to_csv(
        REGISTER_FILE, index=False
    )

st.title("🌊 Interceptor ScaleReady")
st.caption(
    "Independent research prototype for river-cleanup deployment "
    "and sustainable operations."
)

st.info(
    "Research principle: distinguish documented facts from hypotheses "
    "and unknowns. A missing public record does not prove a problem exists."
)


overview, evidence, checklist, sources, dependencies, readiness, actions, report = st.tabs(
    [
        "Research overview",
        "Evidence register",
        "Deployment checklist",
        "Sources & scope",
        "Deployment Dependencies",
        "Readiness Profile",
        "Actions & Handover",
        "Integrated Readiness Report",
    ]
)


with overview:
    st.subheader("Our first research case")
    st.markdown("**Interceptor 003 — Can Tho, Vietnam**")
    st.write(
        "Investigate what public evidence says about operating models, "
        "maintenance, waste handling, financing, and local responsibilities."
    )

    st.subheader("Research progress")

    df = pd.read_csv(REGISTER_FILE)
    total = len(df)
    investigated = int(
        df["Evidence status"].isin(
            ["Supported by source", "Partially supported"]
        ).sum()
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Research questions", total)
    c2.metric("Questions with evidence recorded", investigated)
    c3.metric("Still to investigate", total - investigated)

    st.caption(
        "Progress measures recorded research, not the deployment's "
        "operational readiness."
    )


with evidence:
    st.subheader("Evidence register")
    st.write(
        "Select a research question and use the larger text boxes "
        "to enter complete findings without truncation."
    )

    df = pd.read_csv(REGISTER_FILE).fillna("")

    if not df.empty:
        selected_id = st.selectbox(
            "Select research question",
            df["ID"].tolist(),
            format_func=lambda x: (
                x + " — " +
                df.loc[df["ID"] == x, "Research question"].iloc[0]
            ),
        )

        record = df.loc[df["ID"] == selected_id].iloc[0]

        with st.form("edit_research_record"):
            finding = st.text_area(
                "Finding — enter the complete evidence",
                value=str(record["Finding"]),
                height=150,
                placeholder="Write the finding in full here...",
            )

            source_url = st.text_input(
                "Source URL",
                value=str(record["Source URL"]),
            )

            status_options = [
                "To investigate",
                "Supported by source",
                "Partially supported",
                "Contradicted by source",
                "Unknown",
            ]

            current_status = str(record["Evidence status"])
            if current_status not in status_options:
                current_status = "To investigate"

            status = st.selectbox(
                "Evidence status",
                status_options,
                index=status_options.index(current_status),
            )

            implication = st.text_area(
                "Product implication (optional)",
                value=str(record["Product implication"]),
                height=100,
                placeholder="What might this mean for ScaleReady?",
            )

            save_record = st.form_submit_button(
                "Save this research finding",
                type="primary",
            )

            if save_record:
                df.loc[df["ID"] == selected_id, "Finding"] = finding
                df.loc[df["ID"] == selected_id, "Source URL"] = source_url
                df.loc[df["ID"] == selected_id, "Evidence status"] = status
                df.loc[
                    df["ID"] == selected_id, "Product implication"
                ] = implication

                df.to_csv(REGISTER_FILE, index=False)
                st.success("Research finding saved successfully.")
                st.rerun()

    st.divider()
    st.subheader("All research questions")
    st.dataframe(
        pd.read_csv(REGISTER_FILE).fillna(""),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download register as CSV",
        data=pd.read_csv(REGISTER_FILE).to_csv(
            index=False
        ).encode("utf-8"),
        file_name="interceptor_scaleready_research.csv",
        mime="text/csv",
        key="download_research_register_csv",
    )


with checklist:
    st.subheader("Deployment investigation checklist")
    st.write(
        "These are research areas, not claims that the deployment "
        "has deficiencies."
    )

    checklist_items = [
        "Operating organisation and responsibilities documented",
        "Staffing and operator training arrangements documented",
        "Maintenance process and spare-parts arrangements documented",
        "Waste transport and final destination documented",
        "Operating costs and funding responsibilities documented",
        "Local partner and government commitments documented",
        "Handover conditions and ownership responsibilities documented",
    ]

    for item in checklist_items:
        st.checkbox(item, key="check_" + item)

with sources:
    st.subheader("Starting source")
    st.markdown(
        "[UNDP Vietnam: Towards a Sustainable Financial Model for "
        "Floating Waste Management in Waterways](%s)" % UNDP_URL
    )
    st.write(
        "Use the report to find documented findings, dates, responsible "
        "organisations, financial arrangements, and limitations."
    )

    st.subheader("Research rules")
    st.markdown(
        """
        - Record the exact source for every material finding.
        - Distinguish facts, interpretations, and assumptions.
        - Mark unanswered questions as unknown.
        - Do not invent readiness scores.
        - Validate product opportunities with practitioners.
        """
    )

st.divider()
st.caption(
    "Interceptor ScaleReady | Early-stage independent concept | "
    "Not an official product of The Ocean Cleanup or UNDP."
)


# Deployment Dependencies Tracker
DEPENDENCY_FILE = DATA_DIR / "deployment_dependencies.csv"

DEPENDENCY_COLUMNS = [
    "ID",
    "Requirement",
    "Category",
    "Responsible organisation",
    "Status",
    "Depends on",
    "Evidence or notes",
]

CATEGORY_OPTIONS = [
    "Infrastructure",
    "Funding",
    "Operations",
    "Maintenance",
    "Waste management",
    "Permits and approvals",
    "Handover",
    "Other",
]

STATUS_OPTIONS = [
    "Not assessed",
    "Not started",
    "In progress",
    "Blocked",
    "Complete",
    "Not applicable",
]

if not DEPENDENCY_FILE.exists():
    pd.DataFrame(columns=DEPENDENCY_COLUMNS).to_csv(
        DEPENDENCY_FILE, index=False
    )

# Add any missing columns if this app is opened with an older CSV.
dependency_df = pd.read_csv(DEPENDENCY_FILE).fillna("")
for column in DEPENDENCY_COLUMNS:
    if column not in dependency_df.columns:
        dependency_df[column] = ""
dependency_df = dependency_df[DEPENDENCY_COLUMNS]
dependency_df["ID"] = dependency_df["ID"].astype(str)
dependency_df.to_csv(DEPENDENCY_FILE, index=False)


def next_dependency_id(df):
    """Return the next D### ID without reusing an existing ID."""
    numbers = df["ID"].astype(str).str.extract(r"^D(\d+)$")[0].dropna()
    next_number = int(numbers.astype(int).max()) + 1 if not numbers.empty else 1
    return f"D{next_number:03d}"


def parse_dependency_ids(value):
    """Parse prerequisite tokens separated by commas or semicolons."""
    if not str(value).strip():
        return []
    return [
        item.strip().upper()
        for item in str(value).replace(";", ",").split(",")
        if item.strip()
    ]


with dependencies:
    st.subheader("Deployment Dependencies Tracker")
    st.write(
        "Record requirements, assign owners, link prerequisites by ID, "
        "and capture supporting evidence."
    )
    st.info(
        "Example requirements are planning hypotheses, not claims that "
        "Can Tho has missing infrastructure, funding, or approvals. "
        "In 'Depends on', enter recorded dependency IDs only (for example, "
        "D002, D003), not descriptions such as 'site assessment; funding'. "
        "Add each prerequisite as its own dependency first."
    )

    dependency_df = pd.read_csv(DEPENDENCY_FILE).fillna("")
    for column in DEPENDENCY_COLUMNS:
        if column not in dependency_df.columns:
            dependency_df[column] = ""
    dependency_df = dependency_df[DEPENDENCY_COLUMNS]
    dependency_df["ID"] = dependency_df["ID"].astype(str)

    with st.form("add_dependency"):
        requirement = st.text_input(
            "Requirement",
            placeholder="Example: Complete site assessment",
        )
        category = st.selectbox("Category", CATEGORY_OPTIONS)
        owner = st.text_input(
            "Responsible organisation",
            placeholder="Enter an organisation or Unknown",
        )
        status = st.selectbox("Status", STATUS_OPTIONS)
        depends_on = st.text_input(
            "Depends on (optional)",
            placeholder="Enter existing IDs, e.g. D002, D003",
            help="Use dependency IDs separated by commas or semicolons.",
        )
        notes = st.text_area(
            "Evidence or notes",
            placeholder=(
                "Enter a source URL, documented evidence, or explain "
                "what remains unknown."
            ),
            height=100,
        )
        submitted = st.form_submit_button("Add dependency", type="primary")

        if submitted:
            if not requirement.strip():
                st.error("Please enter a requirement.")
            elif requirement.strip() in dependency_df["Requirement"].astype(str).tolist():
                st.error(
                    "A requirement with this exact name already exists. "
                    "Check the table before adding a duplicate."
                )
            else:
                new_id = next_dependency_id(dependency_df)
                new_row = {
                    "ID": new_id,
                    "Requirement": requirement.strip(),
                    "Category": category,
                    "Responsible organisation": owner.strip() or "Unknown",
                    "Status": status,
                    "Depends on": depends_on.strip(),
                    "Evidence or notes": notes.strip(),
                }
                updated_df = pd.concat(
                    [dependency_df, pd.DataFrame([new_row])],
                    ignore_index=True,
                )
                updated_df[DEPENDENCY_COLUMNS].to_csv(
                    DEPENDENCY_FILE, index=False
                )
                st.success(f"Dependency {new_id} saved.")
                st.rerun()

    st.divider()
    st.subheader("Research Evidence Register")
    st.caption(
        "Record what needs verification, the source consulted, and the next follow-up. "
        "Source type describes where information came from; source quality describes how strongly it supports your specific finding. "
        "An official or peer-reviewed source can still be outdated or irrelevant to a particular claim. "
        "A 'To verify' status does not prove that evidence is absent in the real world."
    )

    evidence_path = DATA_DIR / "research_evidence_register.csv"
    evidence_columns = [
        "Evidence ID",
        "Requirement ID",
        "Evidence question",
        "Claim / finding",
        "Finding classification",
        "Evidence/source URL",
        "Source title or organisation",
        "Publication date",
        "Relevant passage / page",
        "Source type",
        "Source quality",
        "Date checked",
        "Evidence status",
        "Finding / notes",
        "Next follow-up action",
    ]

    if evidence_path.exists():
        try:
            evidence_df = pd.read_csv(evidence_path).fillna("")
        except Exception:
            evidence_df = pd.DataFrame(columns=evidence_columns)
    else:
        evidence_df = pd.DataFrame(columns=evidence_columns)

    for column in evidence_columns:
        if column not in evidence_df.columns:
            evidence_df[column] = ""
    evidence_df = evidence_df[evidence_columns]

    if evidence_df.empty:
        evidence_df = pd.DataFrame(
            [
                {
                    "Evidence ID": "E001",
                    "Requirement ID": "D001",
                    "Evidence question": "What evidence supports the suitability of the proposed unloading location?",
                    "Claim / finding": "",
                    "Finding classification": "Unknown",
                    "Evidence/source URL": "",
                    "Source title or organisation": "",
                    "Source type": "Not yet classified",
                    "Source quality": "Not assessed",
                    "Date checked": "",
                    "Evidence status": "To verify",
                    "Finding / notes": "Research question only; no conclusion recorded yet.",
                    "Next follow-up action": "Identify relevant local site information or a reliable stakeholder/source.",
                },
                {
                    "Evidence ID": "E002",
                    "Requirement ID": "D002",
                    "Evidence question": "What site assessment criteria and supporting evidence are applicable?",
                    "Claim / finding": "",
                    "Finding classification": "Unknown",
                    "Evidence/source URL": "",
                    "Source title or organisation": "",
                    "Source type": "Not yet classified",
                    "Source quality": "Not assessed",
                    "Date checked": "",
                    "Evidence status": "To verify",
                    "Finding / notes": "Research question only; no conclusion recorded yet.",
                    "Next follow-up action": "Find and record relevant assessment criteria and their source.",
                },
                {
                    "Evidence ID": "E003",
                    "Requirement ID": "D003",
                    "Evidence question": "What funding model and ownership arrangements are documented for this scenario?",
                    "Claim / finding": "",
                    "Finding classification": "Unknown",
                    "Evidence/source URL": "",
                    "Source title or organisation": "",
                    "Source type": "Not yet classified",
                    "Source quality": "Not assessed",
                    "Date checked": "",
                    "Evidence status": "To verify",
                    "Finding / notes": "Research question only; no conclusion recorded yet.",
                    "Next follow-up action": "Locate reliable documentation or record that the question remains unanswered.",
                },
            ],
            columns=evidence_columns,
        )

    evidence_df["Publication date"] = (
    evidence_df["Publication date"].fillna("").astype(str)
)
    edited_evidence_df = st.data_editor(
        evidence_df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "Finding classification": st.column_config.SelectboxColumn(
                "Finding classification",
                options=[
                    "Unknown",
                    "Documented fact",
                    "Stakeholder statement",
                    "Hypothesis",
                    "Conflicting findings",
                ],
                required=True,
                help="Classify the finding based on what the source supports; do not label an inference as a documented fact.",
            ),
            "Source type": st.column_config.SelectboxColumn(
                "Source type",
                options=[
                    "Not yet classified",
                    "Official report",
                    "Government publication",
                    "Peer-reviewed study",
                    "Stakeholder statement",
                    "Official organisation webpage",
                    "News article",
                    "Academic / technical report",
                    "Other",
                ],
                required=True,
                help="Classify the source's origin; source type alone does not establish that a claim is correct.",
            ),
            "Source quality": st.column_config.SelectboxColumn(
                "Source quality",
                options=[
                    "Not assessed",
                    "High confidence",
                    "Moderate confidence",
                    "Low confidence",
                    "Conflicting evidence",
                ],
                required=True,
                help="Your assessment of how well this source supports the specific finding. Record the reason in Finding / notes.",
            ),
            "Evidence status": st.column_config.SelectboxColumn(
                "Evidence status",
                options=[
                    "To verify",
                    "Source found",
                    "Evidence recorded",
                    "Needs follow-up",
                    "Unable to verify",
                ],
                required=True,
            ),
            "Publication date": st.column_config.TextColumn(
                "Publication date (YYYY-MM-DD)",
                help="Record the publication date when available; leave blank if unknown.",
            ),
            "Relevant passage / page": st.column_config.TextColumn(
                "Relevant passage / page",
                help="Record a short excerpt, section, or page reference supporting the finding.",
            ),
            "Date checked": st.column_config.TextColumn(
                "Date checked (YYYY-MM-DD)",
                help="Enter the date you checked the source, if applicable.",
            ),
            "Evidence/source URL": st.column_config.LinkColumn(
                "Evidence/source URL",
                help="Paste the source URL when available.",
            ),
        },
        key="research_evidence_editor_v7",
    )

    evidence_col1, evidence_col2 = st.columns(2)
    with evidence_col1:
        if st.button("Save evidence register", key="save_evidence_register_v7"):
            edited_evidence_df = edited_evidence_df.fillna("")
            edited_evidence_df.to_csv(evidence_path, index=False)
            st.success(f"Evidence register saved to {evidence_path}")
    with evidence_col2:
        st.download_button(
            "Download evidence register as CSV",
            data=edited_evidence_df.fillna("").to_csv(index=False).encode("utf-8"),
            file_name="scaleready_research_evidence_register.csv",
            mime="text/csv",
            key="download_evidence_register_v7",
        )

    st.subheader("Evidence Quality Summary")
    st.caption(
        "Counts below summarise the entries in your evidence register. They describe research tracking "
        "progress, not the readiness of a real-world deployment."
    )

    saved_evidence_path = DATA_DIR / "research_evidence_register.csv"
    summary_source_df = edited_evidence_df.copy().fillna("")
    if saved_evidence_path.exists():
        try:
            persisted_evidence_df = pd.read_csv(saved_evidence_path).fillna("")
            if not persisted_evidence_df.empty:
                # Use saved records when available so the summary reflects the persisted register.
                summary_source_df = persisted_evidence_df
        except Exception:
            pass

    if summary_source_df.empty:
        st.info("No evidence entries are recorded yet.")
    else:
        status_series = summary_source_df.get(
            "Evidence status", pd.Series(dtype=str)
        ).fillna("").astype(str).str.strip()
        quality_series = summary_source_df.get(
            "Source quality", pd.Series(dtype=str)
        ).fillna("").astype(str).str.strip()

        total_entries = len(summary_source_df)
        assessed_count = int(
            quality_series.isin(["High confidence", "Moderate confidence", "Low confidence"]).sum()
        )
        unverified_count = int(status_series.isin(["To verify", "Unable to verify"]).sum())
        conflict_count = int((quality_series == "Conflicting evidence").sum())
        not_assessed_count = int((quality_series == "Not assessed").sum())

        summary_cols = st.columns(4)
        summary_cols[0].metric("Evidence entries", total_entries)
        summary_cols[1].metric("Quality assessed", assessed_count)
        summary_cols[2].metric("Unverified / unable to verify", unverified_count)
        summary_cols[3].metric("Conflicting evidence", conflict_count)

        quality_counts = (
            quality_series.replace("", "Not assessed")
            .value_counts()
            .rename_axis("Source quality")
            .reset_index(name="Entries")
        )
        st.dataframe(quality_counts, use_container_width=True, hide_index=True)

        if conflict_count:
            st.warning(
                f"{conflict_count} entry/entries are marked 'Conflicting evidence'. "
                "Review the competing sources and record what remains uncertain."
            )
        if not_assessed_count:
            st.info(
                f"{not_assessed_count} entry/entries have source quality 'Not assessed'. "
                "Assess relevance, recency, methodology, and how directly the source supports the finding."
            )
        if unverified_count:
            st.info(
                f"{unverified_count} entry/entries have evidence status 'To verify' or 'Unable to verify'. "
                "These are research tracking states, not proof that evidence is absent."
            )

    st.subheader("Source-to-Claim Traceability")
    st.caption(
        "This view connects a recorded claim or finding to its requirement and source details. "
        "Only classify a finding as a documented fact when the cited source directly supports it."
    )

    trace_df = summary_source_df.copy().fillna("")
    for column in evidence_columns:
        if column not in trace_df.columns:
            trace_df[column] = ""
    trace_df = trace_df.reindex(columns=evidence_columns)

    trace_columns = [
        "Evidence ID",
        "Requirement ID",
        "Claim / finding",
        "Finding classification",
        "Evidence/source URL",
        "Source title or organisation",
        "Publication date",
        "Relevant passage / page",
        "Source type",
        "Source quality",
        "Evidence status",
    ]
    trace_view = trace_df[trace_columns].copy()
    trace_view = trace_view[
        trace_view["Claim / finding"].astype(str).str.strip().ne("")
        | trace_view["Evidence/source URL"].astype(str).str.strip().ne("")
    ]

    if trace_view.empty:
        st.info(
            "No claims have been linked to source details yet. Add a claim/finding and its source "
            "in the Research Evidence Register, then save the register."
        )
    else:
        st.dataframe(trace_view, use_container_width=True, hide_index=True)
        st.download_button(
            "Download source-to-claim traceability as CSV",
            data=trace_view.to_csv(index=False).encode("utf-8"),
            file_name="scaleready_source_to_claim_traceability.csv",
            mime="text/csv",
            key="download_source_claim_traceability_v10",
        )

    st.divider()

    st.subheader("Manage dependencies")
    st.caption(
        "Edit cells directly, then select Save changes. Keep IDs unchanged. "
        "For prerequisite links, use IDs such as D002, D003."
    )

    dependency_df = pd.read_csv(DEPENDENCY_FILE).fillna("")
    for column in DEPENDENCY_COLUMNS:
        if column not in dependency_df.columns:
            dependency_df[column] = ""
    dependency_df = dependency_df[DEPENDENCY_COLUMNS]
    dependency_df["ID"] = dependency_df["ID"].astype(str)

    if dependency_df.empty:
        st.info("No dependencies have been added yet.")
    else:
        edited_dependencies = st.data_editor(
            dependency_df,
            num_rows="fixed",
            use_container_width=True,
            hide_index=True,
            key="editable_dependencies_v2",
            column_config={
                "ID": st.column_config.TextColumn("ID", disabled=True),
                "Requirement": st.column_config.TextColumn(
                    "Requirement", required=True
                ),
                "Category": st.column_config.SelectboxColumn(
                    "Category", options=CATEGORY_OPTIONS, required=True
                ),
                "Responsible organisation": st.column_config.TextColumn(
                    "Responsible organisation"
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Status", options=STATUS_OPTIONS, required=True
                ),
                "Depends on": st.column_config.TextColumn(
                    "Depends on",
                    help="Existing prerequisite IDs separated by commas, e.g. D002, D003.",
                ),
                "Evidence or notes": st.column_config.TextColumn(
                    "Evidence or notes"
                ),
            },
        )

        if st.button("Save changes", type="primary", key="save_dependencies_v2"):
            edited_ids = edited_dependencies["ID"].astype(str).str.strip()
            if edited_ids.duplicated().any():
                st.error("Duplicate IDs detected. IDs must be unique; changes were not saved.")
            elif edited_dependencies["Requirement"].astype(str).str.strip().eq("").any():
                st.error("Every dependency must have a requirement. Changes were not saved.")
            else:
                edited_dependencies[DEPENDENCY_COLUMNS].to_csv(
                    DEPENDENCY_FILE, index=False
                )
                st.success("Dependency changes saved.")
                st.rerun()

        current_dependencies = pd.read_csv(DEPENDENCY_FILE).fillna("")
        st.download_button(
            "Download dependencies as CSV",
            data=current_dependencies[DEPENDENCY_COLUMNS].to_csv(
                index=False
            ).encode("utf-8"),
            file_name="interceptor_scaleready_dependencies.csv",
            mime="text/csv",
            key="download_dependencies_v2",
        )

    st.divider()
    st.subheader("Validation & attention report")

    validation_df = pd.read_csv(DEPENDENCY_FILE).fillna("")
    for column in DEPENDENCY_COLUMNS:
        if column not in validation_df.columns:
            validation_df[column] = ""
    validation_df = validation_df[DEPENDENCY_COLUMNS]
    validation_df["ID"] = validation_df["ID"].astype(str)

    attention_items = []
    if validation_df.empty:
        st.info("Add a dependency to begin validation.")
    else:
        known_ids = set(validation_df["ID"].astype(str).str.strip())
        status_by_id = dict(
            zip(
                validation_df["ID"].astype(str).str.strip(),
                validation_df["Status"].astype(str).str.strip(),
            )
        )

        for _, row in validation_df.iterrows():
            dependency_id = str(row["ID"]).strip()
            requirement_text = str(row["Requirement"]).strip()
            owner_value = str(row["Responsible organisation"]).strip()
            status_value = str(row["Status"]).strip()
            evidence_value = str(row["Evidence or notes"]).strip()
            prerequisite_ids = parse_dependency_ids(row["Depends on"])

            def add_flag(issue, reason, action):
                attention_items.append({
                    "ID": dependency_id,
                    "Requirement": requirement_text,
                    "Issue": issue,
                    "Reason": reason,
                    "Suggested action": action,
                })

            if not owner_value or owner_value.lower() == "unknown":
                add_flag(
                    "Research gap: owner unknown",
                    "No responsible organisation is recorded. This is an information gap, not proof that no owner exists.",
                    "Verify the responsible organisation from a source or stakeholder confirmation; keep Unknown until verified.",
                )

            if not evidence_value:
                add_flag(
                    "Research gap: evidence not recorded",
                    "The evidence/notes field is empty. This does not establish that supporting evidence or arrangements do not exist.",
                    "Add a source, supporting evidence, or a note explaining what remains unknown.",
                )

            if status_value == "Blocked":
                add_flag(
                    "Reported status: blocked",
                    "This requirement is marked Blocked in the tracker. Confirm the blocker and its impact before treating it as a verified operational blocker.",
                    "Record the evidence for the blocker, its impact, the responsible party, and the next action.",
                )
            elif status_value == "Not assessed":
                add_flag(
                    "Research gap: assessment pending",
                    "The requirement has not yet been assessed; its real-world state is unknown.",
                    "Review available evidence or consult a relevant stakeholder, then record the assessment and source.",
                )

            seen_prerequisites = set()
            for prerequisite_id in prerequisite_ids:
                if not pd.Series([prerequisite_id]).str.fullmatch(r"D\d+", na=False).iloc[0]:
                    add_flag(
                        "Prerequisite must use a dependency ID",
                        f"'{prerequisite_id}' is descriptive text, not a recorded ID such as D002.",
                        "Create a separate dependency for this prerequisite, then reference its ID (for example, D002).",
                    )
                    continue

                if prerequisite_id == dependency_id:
                    add_flag(
                        "Self-dependency",
                        f"{dependency_id} lists itself as a prerequisite.",
                        "Remove the self-reference and identify the actual prerequisite.",
                    )
                    continue

                if prerequisite_id in seen_prerequisites:
                    add_flag(
                        "Duplicate prerequisite link",
                        f"{prerequisite_id} is listed more than once.",
                        "Keep only one link to this prerequisite.",
                    )
                    continue
                seen_prerequisites.add(prerequisite_id)

                if prerequisite_id not in known_ids:
                    add_flag(
                        "Unknown prerequisite ID",
                        f"{prerequisite_id} does not match a recorded dependency ID.",
                        f"Create {prerequisite_id} or correct the prerequisite ID.",
                    )
                else:
                    prerequisite_status = status_by_id.get(prerequisite_id, "")
                    if prerequisite_status not in ("Complete", "Not applicable"):
                        add_flag(
                            "Dependency needs review",
                            f"{prerequisite_id} currently has status '{prerequisite_status}'. This does not by itself prove the prerequisite is an operational blocker.",
                            f"Assess {prerequisite_id} using evidence. Confirm whether it must be completed before this requirement can proceed.",
                        )

        # Classify attention items to help reviewers triage work.
        # Priority describes the type of follow-up needed, not deployment readiness.
        priority_by_issue = {
            "Reported status: blocked": "Verify potential blocker",
            "Dependency needs review": "Dependency review",
            "Research gap: owner unknown": "Information gap",
            "Research gap: evidence not recorded": "Information gap",
            "Research gap: assessment pending": "Assessment required",
            "Self-dependency": "Data correction",
            "Duplicate prerequisite link": "Data correction",
            "Unknown prerequisite ID": "Data correction",
            "Prerequisite must use a dependency ID": "Data correction",
        }
        for item in attention_items:
            item["Priority classification"] = priority_by_issue.get(
                item["Issue"], "Review required"
            )

        c1, c2 = st.columns(2)
        c1.metric("Requirements recorded", len(validation_df))
        c2.metric("Attention items", len(attention_items))

        # Priority Summary Dashboard: classify follow-up work, not deployment risk.
        priority_order = [
            "Verify potential blocker",
            "Dependency review",
            "Assessment required",
            "Information gap",
            "Data correction",
            "Review required",
        ]
        priority_counts = {
            priority: sum(
                1 for item in attention_items
                if item.get("Priority classification") == priority
            )
            for priority in priority_order
        }
        summary_df = pd.DataFrame(
            [
                {"Priority classification": priority, "Items": count}
                for priority, count in priority_counts.items()
                if count > 0
            ]
        )

        st.subheader("Priority Summary Dashboard")
        st.caption(
            "This summary prioritises follow-up actions. It is not a risk score "
            "and does not certify deployment readiness."
        )

        if attention_items:
            metric_cols = st.columns(min(4, max(1, len(summary_df))))
            for index, (_, summary_row) in enumerate(summary_df.head(4).iterrows()):
                metric_cols[index].metric(
                    str(summary_row["Priority classification"]),
                    int(summary_row["Items"]),
                )

            with st.expander("View classification breakdown"):
                st.dataframe(
                    summary_df,
                    use_container_width=True,
                    hide_index=True,
                )

            available_filters = ["All classifications"] + summary_df[
                "Priority classification"
            ].tolist()
            selected_priority = st.selectbox(
                "Filter attention items",
                available_filters,
                key="attention_priority_filter_v5",
            )
            if selected_priority == "All classifications":
                filtered_attention_df = pd.DataFrame(attention_items)
            else:
                filtered_attention_df = pd.DataFrame(
                    [
                        item for item in attention_items
                        if item.get("Priority classification") == selected_priority
                    ]
                )
        else:
            st.success(
                "No attention flags were triggered by these rules. "
                "This is not a certification of deployment readiness."
            )
            filtered_attention_df = pd.DataFrame()

        if attention_items:
            st.subheader("Recommended Next Actions")
            st.caption(
                "These are suggested research and planning steps generated from the tracker. "
                "They do not assert that the real-world deployment has a deficiency."
            )

            action_rows = []
            seen_actions = set()
            for item in attention_items:
                issue = item.get("Issue", "")
                dependency_id = item.get("ID", "")
                requirement = item.get("Requirement", "")
                suggested = item.get("Suggested action", "")
                if issue == "Research gap: owner unknown":
                    action = (
                        f"Verify the responsible organisation for {dependency_id} "
                        f"({requirement}) using a reliable source or stakeholder confirmation."
                    )
                elif issue == "Research gap: assessment pending":
                    action = (
                        f"Assess {dependency_id} ({requirement}) using available evidence "
                        "and record the source and conclusion."
                    )
                elif issue == "Dependency needs review":
                    action = (
                        f"Review prerequisite {suggested.split('Assess ', 1)[-1]} "
                        if suggested.startswith("Assess ")
                        else f"Review the prerequisite for {dependency_id}: {suggested}"
                    )
                elif issue == "Research gap: evidence not recorded":
                    action = (
                        f"Add a source or an explicit note about what remains unknown for "
                        f"{dependency_id} ({requirement})."
                    )
                elif issue == "Reported status: blocked":
                    action = (
                        f"Verify the reported blocker for {dependency_id} ({requirement}) "
                        "and document evidence, impact, responsible party, and next step."
                    )
                elif issue in {
                    "Self-dependency",
                    "Duplicate prerequisite link",
                    "Unknown prerequisite ID",
                    "Prerequisite must use a dependency ID",
                }:
                    action = f"Correct the dependency link for {dependency_id}: {suggested}"
                else:
                    action = suggested or f"Review {dependency_id} ({requirement})."

                unique_key = (dependency_id, action)
                if unique_key not in seen_actions:
                    seen_actions.add(unique_key)
                    action_rows.append({
                        "Requirement ID": dependency_id,
                        "Requirement": requirement,
                        "Recommended next action": action,
                        "Classification": item.get(
                            "Priority classification", "Review required"
                        ),
                    })

            actions_df = pd.DataFrame(action_rows)
            st.dataframe(
                actions_df,
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                "Download recommended actions as CSV",
                data=actions_df.to_csv(index=False).encode("utf-8"),
                file_name="scaleready_recommended_next_actions.csv",
                mime="text/csv",
                key="download_recommended_actions_v6",
            )

            st.warning(
                "Priority classification guides follow-up; it is not a risk score or readiness rating. "
                "A missing owner, missing evidence, or 'Not assessed' status means the information is unknown—not that the arrangement is absent. "
                "Treat a blocker as confirmed only when supported by evidence."
            )
            st.dataframe(
                filtered_attention_df,
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                "Download filtered attention report as CSV",
                data=filtered_attention_df.to_csv(index=False).encode("utf-8"),
                file_name="scaleready_attention_report.csv",
                mime="text/csv",
                key="download_attention_report_v2",
            )


# Deployment Readiness Profile (v11)
READINESS_FILE = DATA_DIR / "deployment_readiness_profile.csv"
READINESS_COLUMNS = [
    "Profile ID",
    "Readiness area",
    "Assessment question",
    "Assessment status",
    "Responsible organisation",
    "Linked evidence IDs",
    "Assessment notes",
    "Next action",
    "Last reviewed",
]
READINESS_AREAS = [
    "Unloading location and site suitability",
    "Waste transfer, transport and downstream handling",
    "Operating ownership and decision rights",
    "Routine maintenance and repairs",
    "Power, connectivity and site access",
    "Permits, approvals and compliance",
    "Funding and operating cost model",
    "Local training and operational capability",
    "Performance monitoring and escalation",
    "Handover and continuity arrangements",
]
READINESS_STATUSES = [
    "Not assessed",
    "Evidence found — review needed",
    "Supported by evidence",
    "Partially supported",
    "Conflicting evidence",
    "Gap confirmed by evidence",
    "Not applicable — evidence recorded",
]

if not READINESS_FILE.exists():
    starter_profile = []
    for i, area in enumerate(READINESS_AREAS, start=1):
        starter_profile.append({
            "Profile ID": f"RP{i:03d}",
            "Readiness area": area,
            "Assessment question": {
                "Unloading location and site suitability": "Is the proposed unloading location identified, accessible, and supported by a documented site assessment?",
                "Waste transfer, transport and downstream handling": "What documented process moves collected waste from unloading to its next handling or processing destination?",
                "Operating ownership and decision rights": "Which organisation owns day-to-day operation and makes operational decisions?",
                "Routine maintenance and repairs": "What maintenance schedule, responsible party, spare-parts process, and repair escalation are documented?",
                "Power, connectivity and site access": "What site requirements for power, connectivity, access, and safe servicing are documented?",
                "Permits, approvals and compliance": "Which permits, approvals, or regulatory obligations apply, and what evidence confirms their status?",
                "Funding and operating cost model": "What evidence describes installation, operating, maintenance, waste-handling, and long-term funding costs?",
                "Local training and operational capability": "What training, operating procedures, and local support capabilities are documented?",
                "Performance monitoring and escalation": "Which performance indicators, reporting responsibilities, and escalation procedures are documented?",
                "Handover and continuity arrangements": "What documented plan covers handover, accountability, continuity of service, and unresolved actions?",
            }[area],
            "Assessment status": "Not assessed",
            "Responsible organisation": "",
            "Linked evidence IDs": "",
            "Assessment notes": "",
            "Next action": "Identify and review relevant evidence; do not infer a gap from missing information.",
            "Last reviewed": "",
        })
    pd.DataFrame(starter_profile, columns=READINESS_COLUMNS).to_csv(READINESS_FILE, index=False)

# Migrate older profile files safely without replacing saved user entries.
readiness_df = pd.read_csv(READINESS_FILE).fillna("")
for column in READINESS_COLUMNS:
    if column not in readiness_df.columns:
        readiness_df[column] = ""
readiness_df = readiness_df[READINESS_COLUMNS]
if not readiness_df.empty:
    readiness_df["Profile ID"] = readiness_df["Profile ID"].astype(str)
    readiness_df.to_csv(READINESS_FILE, index=False)

with readiness:
    st.subheader("Deployment Readiness Profile")
    st.write(
        "Assess whether the information needed to plan and sustain a deployment is documented. "
        "This is a research checklist, not an official assessment of Interceptor 003 or any actual site."
    )
    st.warning(
        "Important: 'Not assessed' means information has not yet been reviewed. It does not mean a real-world gap exists. "
        "Use 'Gap confirmed by evidence' only when a source directly supports that conclusion."
    )
    st.caption(
        "Starter questions are prompts for investigation. Link evidence using IDs from the Research Evidence Register, "
        "for example E001. Record uncertainty and the next action rather than guessing."
    )

    current_profile = pd.read_csv(READINESS_FILE).fillna("")
    for column in READINESS_COLUMNS:
        if column not in current_profile.columns:
            current_profile[column] = ""
    current_profile = current_profile[READINESS_COLUMNS]

    status_series = current_profile["Assessment status"].astype(str).str.strip()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Readiness areas", len(current_profile))
    c2.metric("Not assessed", int((status_series == "Not assessed").sum()))
    c3.metric("Supported by evidence", int((status_series == "Supported by evidence").sum()))
    c4.metric("Confirmed gaps", int((status_series == "Gap confirmed by evidence").sum()))

    edited_profile = st.data_editor(
        current_profile,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        key="readiness_profile_editor_v11",
        column_config={
            "Profile ID": st.column_config.TextColumn("Profile ID", disabled=True),
            "Readiness area": st.column_config.TextColumn("Readiness area", disabled=True),
            "Assessment question": st.column_config.TextColumn("Assessment question", disabled=True, width="large"),
            "Assessment status": st.column_config.SelectboxColumn("Assessment status", options=READINESS_STATUSES, required=True),
            "Responsible organisation": st.column_config.TextColumn("Responsible organisation"),
            "Linked evidence IDs": st.column_config.TextColumn("Linked evidence IDs", help="Use evidence IDs, e.g. E001, E002."),
            "Assessment notes": st.column_config.TextColumn("Assessment notes", width="large"),
            "Next action": st.column_config.TextColumn("Next action", width="large"),
            "Last reviewed": st.column_config.TextColumn("Last reviewed", help="Use YYYY-MM-DD."),
        },
    )

    if st.button("Save readiness profile", type="primary", key="save_readiness_profile_v11"):
        ids = edited_profile["Profile ID"].astype(str).str.strip()
        if ids.duplicated().any():
            st.error("Duplicate Profile IDs detected. The profile was not saved.")
        elif not edited_profile["Assessment status"].astype(str).isin(READINESS_STATUSES).all():
            st.error("One or more assessment statuses are invalid. The profile was not saved.")
        else:
            edited_profile[READINESS_COLUMNS].to_csv(READINESS_FILE, index=False)
            st.success("Deployment Readiness Profile saved.")
            st.rerun()

    saved_profile = pd.read_csv(READINESS_FILE).fillna("")
    st.download_button(
        "Download readiness profile as CSV",
        data=saved_profile[READINESS_COLUMNS].to_csv(index=False).encode("utf-8"),
        file_name="interceptor_scaleready_deployment_readiness_profile.csv",
        mime="text/csv",
        key="download_readiness_profile_v11",
    )
    st.caption(
        "No single overall readiness score is calculated in this version. The profile is intended to expose "
        "what is known, what remains uncertain, and what evidence or action is needed next."
    )



# Operational Action & Handover Workflow (v12)
ACTION_FILE = DATA_DIR / "operational_actions.csv"
ACTION_COLUMNS = [
    "Action ID",
    "Action title",
    "Linked readiness area ID",
    "Linked evidence IDs",
    "Action description / expected outcome",
    "Responsible organisation / owner",
    "Target date",
    "Prerequisite action IDs",
    "Status",
    "Handover / acceptance notes",
    "Completion evidence / URL",
    "Last updated",
]
ACTION_STATUSES = [
    "Open",
    "In progress",
    "Waiting on prerequisite",
    "Blocked",
    "Ready for handover",
    "Completed",
    "Cancelled",
]

if not ACTION_FILE.exists():
    pd.DataFrame(columns=ACTION_COLUMNS).to_csv(ACTION_FILE, index=False)


def next_action_id(df):
    """Return the next A### identifier without reusing existing IDs."""
    if df.empty or "Action ID" not in df.columns:
        return "A001"
    numbers = df["Action ID"].astype(str).str.extract(r"^A(\d+)$")[0].dropna()
    next_number = int(numbers.astype(int).max()) + 1 if not numbers.empty else 1
    return f"A{next_number:03d}"


def parse_action_ids(value):
    """Parse action IDs separated by commas or semicolons."""
    if not str(value).strip():
        return []
    return [
        token.strip().upper()
        for token in str(value).replace(";", ",").split(",")
        if token.strip()
    ]


# Read existing actions and safely add columns introduced in future versions.
action_df = pd.read_csv(ACTION_FILE).fillna("")
for column in ACTION_COLUMNS:
    if column not in action_df.columns:
        action_df[column] = ""
action_df = action_df[ACTION_COLUMNS]
action_df["Action ID"] = action_df["Action ID"].astype(str)
action_df.to_csv(ACTION_FILE, index=False)

with actions:
    st.subheader("Operational Action & Handover Workflow")
    st.write(
        "Turn a readiness finding or unanswered question into an owned action. "
        "Track prerequisites, target dates, status, and what another team needs "
        "to accept during handover."
    )
    st.info(
        "Use this tracker for planning and follow-up. An open action or missing "
        "owner is not, by itself, proof of a real-world operational deficiency. "
        "Only mark an action blocked when the dependency or issue is known."
    )

    profile_for_actions = pd.read_csv(READINESS_FILE).fillna("")
    readiness_choices = [""]
    readiness_labels = {"": "Not linked"}
    if not profile_for_actions.empty:
        for _, row in profile_for_actions.iterrows():
            rid = str(row.get("Profile ID", "")).strip()
            area = str(row.get("Readiness area", "")).strip()
            if rid:
                readiness_choices.append(rid)
                readiness_labels[rid] = f"{rid} — {area}"

    evidence_path_for_actions = DATA_DIR / "research_evidence_register.csv"
    if evidence_path_for_actions.exists():
        try:
            ev_for_actions = pd.read_csv(evidence_path_for_actions).fillna("")
            evidence_ids = [str(x).strip() for x in ev_for_actions.get("Evidence ID", pd.Series(dtype=str)).tolist() if str(x).strip()]
        except Exception:
            evidence_ids = []
    else:
        evidence_ids = []

    existing_action_df = pd.read_csv(ACTION_FILE).fillna("")
    for column in ACTION_COLUMNS:
        if column not in existing_action_df.columns:
            existing_action_df[column] = ""
    existing_action_df = existing_action_df[ACTION_COLUMNS]
    existing_action_df["Action ID"] = existing_action_df["Action ID"].astype(str)
    known_action_ids = set(existing_action_df["Action ID"].astype(str).str.strip())

    st.subheader("Action overview")
    status_counts = existing_action_df["Status"].astype(str).str.strip()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Actions", len(existing_action_df))
    m2.metric("Open / in progress", int(status_counts.isin(["Open", "In progress"]).sum()))
    m3.metric("Blocked / waiting", int(status_counts.isin(["Blocked", "Waiting on prerequisite"]).sum()))
    m4.metric("Ready for handover", int((status_counts == "Ready for handover").sum()))

    with st.expander("Add a follow-up action", expanded=existing_action_df.empty):
        with st.form("add_operational_action_v12"):
            action_title = st.text_input("Action title", placeholder="Example: Confirm waste-transfer receiving arrangements")
            linked_readiness = st.selectbox(
                "Linked readiness area (optional)",
                readiness_choices,
                format_func=lambda value: readiness_labels.get(value, value),
            )
            linked_evidence = st.text_input(
                "Linked evidence IDs (optional)",
                placeholder="Example: E001, E003",
                help="Use existing Evidence IDs separated by commas or semicolons.",
            )
            action_description = st.text_area(
                "Action description / expected outcome",
                placeholder="Describe the follow-up and what would count as a useful outcome.",
                height=90,
            )
            action_owner = st.text_input(
                "Responsible organisation / owner",
                placeholder="Enter a confirmed owner, or Unknown",
            )
            action_target = st.text_input(
                "Target date (YYYY-MM-DD, optional)",
                placeholder="YYYY-MM-DD",
            )
            prerequisite_ids = st.text_input(
                "Prerequisite action IDs (optional)",
                placeholder="Example: A001, A002",
                help="Use existing Action IDs. Add prerequisite actions before linking them.",
            )
            action_status = st.selectbox("Status", ACTION_STATUSES, index=0)
            handover_notes = st.text_area(
                "Handover / acceptance notes (optional)",
                placeholder="Who needs to accept the outcome, and what should they receive?",
                height=80,
            )
            completion_url = st.text_input(
                "Completion evidence / URL (optional)",
                placeholder="URL or evidence reference to add when completed",
            )
            add_action = st.form_submit_button("Add action", type="primary")

            if add_action:
                errors = []
                if not action_title.strip():
                    errors.append("Enter an action title.")
                if action_target.strip():
                    try:
                        pd.to_datetime(action_target.strip(), format="%Y-%m-%d", errors="raise")
                    except (ValueError, TypeError):
                        errors.append("Target date must use YYYY-MM-DD, or be left blank.")
                prerequisites = parse_action_ids(prerequisite_ids)
                unknown_prerequisites = [x for x in prerequisites if x not in known_action_ids]
                if unknown_prerequisites:
                    errors.append("Unknown prerequisite action ID(s): " + ", ".join(unknown_prerequisites))
                linked_ids = parse_action_ids(linked_evidence)
                if evidence_ids:
                    unknown_evidence = [x for x in linked_ids if x not in evidence_ids]
                    if unknown_evidence:
                        errors.append("Unknown evidence ID(s): " + ", ".join(unknown_evidence))
                if errors:
                    for message in errors:
                        st.error(message)
                else:
                    new_action_id = next_action_id(existing_action_df)
                    new_row = {
                        "Action ID": new_action_id,
                        "Action title": action_title.strip(),
                        "Linked readiness area ID": linked_readiness,
                        "Linked evidence IDs": ", ".join(linked_ids),
                        "Action description / expected outcome": action_description.strip(),
                        "Responsible organisation / owner": action_owner.strip() or "Unknown",
                        "Target date": action_target.strip(),
                        "Prerequisite action IDs": ", ".join(prerequisites),
                        "Status": action_status,
                        "Handover / acceptance notes": handover_notes.strip(),
                        "Completion evidence / URL": completion_url.strip(),
                        "Last updated": pd.Timestamp.today().strftime("%Y-%m-%d"),
                    }
                    updated_actions = pd.concat([existing_action_df, pd.DataFrame([new_row])], ignore_index=True)
                    updated_actions[ACTION_COLUMNS].to_csv(ACTION_FILE, index=False)
                    st.success(f"Action {new_action_id} saved.")
                    st.rerun()

    st.divider()
    st.subheader("Review and update actions")
    st.caption(
        "Edit the fields in the table, then save. Action IDs are locked to preserve links. "
        "Use prerequisite IDs only for actions that already exist; avoid circular dependencies."
    )
    current_actions = pd.read_csv(ACTION_FILE).fillna("")
    for column in ACTION_COLUMNS:
        if column not in current_actions.columns:
            current_actions[column] = ""
    current_actions = current_actions[ACTION_COLUMNS]
    current_actions["Action ID"] = current_actions["Action ID"].astype(str)

    edited_actions = st.data_editor(
        current_actions,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        key="operational_actions_editor_v12",
        column_config={
            "Action ID": st.column_config.TextColumn("Action ID", disabled=True),
            "Action title": st.column_config.TextColumn("Action title", required=True, width="large"),
            "Linked readiness area ID": st.column_config.SelectboxColumn("Linked readiness area ID", options=readiness_choices),
            "Linked evidence IDs": st.column_config.TextColumn("Linked evidence IDs", help="Existing evidence IDs separated by commas."),
            "Action description / expected outcome": st.column_config.TextColumn("Action description / expected outcome", width="large"),
            "Responsible organisation / owner": st.column_config.TextColumn("Responsible organisation / owner"),
            "Target date": st.column_config.TextColumn("Target date", help="YYYY-MM-DD or blank."),
            "Prerequisite action IDs": st.column_config.TextColumn("Prerequisite action IDs", help="Existing Action IDs separated by commas."),
            "Status": st.column_config.SelectboxColumn("Status", options=ACTION_STATUSES, required=True),
            "Handover / acceptance notes": st.column_config.TextColumn("Handover / acceptance notes", width="large"),
            "Completion evidence / URL": st.column_config.TextColumn("Completion evidence / URL", width="large"),
            "Last updated": st.column_config.TextColumn("Last updated", disabled=True),
        },
    )

    if st.button("Save action updates", type="primary", key="save_operational_actions_v12"):
        errors = []
        ids = edited_actions["Action ID"].astype(str).str.strip()
        if ids.duplicated().any():
            errors.append("Duplicate Action IDs detected; updates were not saved.")
        if edited_actions["Action title"].astype(str).str.strip().eq("").any():
            errors.append("Every action must have a title.")
        valid_status = edited_actions["Status"].astype(str).isin(ACTION_STATUSES).all()
        if not valid_status:
            errors.append("One or more action statuses are invalid.")
        allowed_ids = set(ids)
        for _, row in edited_actions.iterrows():
            aid = str(row["Action ID"]).strip()
            target = str(row["Target date"]).strip()
            if target:
                try:
                    pd.to_datetime(target, format="%Y-%m-%d", errors="raise")
                except (ValueError, TypeError):
                    errors.append(f"{aid}: target date must use YYYY-MM-DD or be blank.")
            prerequisites = parse_action_ids(row["Prerequisite action IDs"])
            if aid in prerequisites:
                errors.append(f"{aid}: an action cannot depend on itself.")
            unknown = [x for x in prerequisites if x not in allowed_ids]
            if unknown:
                errors.append(f"{aid}: unknown prerequisite action ID(s): " + ", ".join(unknown))
            linked_ids = parse_action_ids(row["Linked evidence IDs"])
            if evidence_ids:
                unknown_evidence = [x for x in linked_ids if x not in evidence_ids]
                if unknown_evidence:
                    errors.append(f"{aid}: unknown evidence ID(s): " + ", ".join(unknown_evidence))
        if errors:
            for message in errors:
                st.error(message)
        else:
            edited_actions = edited_actions[ACTION_COLUMNS].copy()
            edited_actions["Last updated"] = pd.Timestamp.today().strftime("%Y-%m-%d")
            edited_actions.to_csv(ACTION_FILE, index=False)
            st.success("Action updates saved successfully.")
            st.rerun()

    saved_actions = pd.read_csv(ACTION_FILE).fillna("")
    st.download_button(
        "Download actions & handover as CSV",
        data=saved_actions[ACTION_COLUMNS].to_csv(index=False).encode("utf-8"),
        file_name="interceptor_scaleready_actions_handover.csv",
        mime="text/csv",
        key="download_actions_handover_v12",
    )
    st.caption(
        "This version records prerequisites and warns about unknown IDs and self-dependencies. "
        "It does not yet automatically calculate full dependency chains, detect every possible circular dependency, "
        "or approve a real-world handover. Those decisions require human review and supporting evidence."
    )


# Integrated Readiness Report (v13)
with report:
    st.subheader("Integrated Deployment Readiness Report")
    st.write(
        "A consolidated view of recorded readiness assessments, research evidence, "
        "deployment dependencies, and follow-up actions. This report summarises saved "
        "records; it does not independently certify operational readiness."
    )

    # Reload persisted files so the report reflects saved data, not stale form values.
    research_report = pd.read_csv(REGISTER_FILE).fillna("") if REGISTER_FILE.exists() else pd.DataFrame()
    evidence_report_path = DATA_DIR / "research_evidence_register.csv"
    evidence_report = pd.read_csv(evidence_report_path).fillna("") if evidence_report_path.exists() else pd.DataFrame()
    dependencies_report = pd.read_csv(DEPENDENCY_FILE).fillna("") if DEPENDENCY_FILE.exists() else pd.DataFrame()
    readiness_report = pd.read_csv(READINESS_FILE).fillna("") if READINESS_FILE.exists() else pd.DataFrame()
    actions_report = pd.read_csv(ACTION_FILE).fillna("") if ACTION_FILE.exists() else pd.DataFrame()

    total_areas = len(readiness_report)
    assessed_statuses = ["Evidence found — review needed", "Supported by evidence", "Partially supported", "Conflicting evidence", "Gap confirmed by evidence", "Not applicable — evidence recorded"]
    assessed_count = int(readiness_report["Assessment status"].isin(assessed_statuses).sum()) if total_areas and "Assessment status" in readiness_report else 0
    review_needed_count = int((readiness_report["Assessment status"] == "Evidence found — review needed").sum()) if total_areas and "Assessment status" in readiness_report else 0
    supported_count = int((readiness_report["Assessment status"] == "Supported by evidence").sum()) if total_areas and "Assessment status" in readiness_report else 0
    partially_supported_count = int((readiness_report["Assessment status"] == "Partially supported").sum()) if total_areas and "Assessment status" in readiness_report else 0
    conflicting_count = int((readiness_report["Assessment status"] == "Conflicting evidence").sum()) if total_areas and "Assessment status" in readiness_report else 0
    confirmed_gap_count = int((readiness_report["Assessment status"] == "Gap confirmed by evidence").sum()) if total_areas and "Assessment status" in readiness_report else 0
    open_action_count = int((~actions_report["Status"].isin(["Completed", "Cancelled"])).sum()) if len(actions_report) and "Status" in actions_report else 0
    blocked_action_count = int(actions_report["Status"].isin(["Blocked", "Waiting on prerequisite"]).sum()) if len(actions_report) and "Status" in actions_report else 0
    dependency_open_count = int((~dependencies_report["Status"].isin(["Complete", "Not applicable"])).sum()) if len(dependencies_report) and "Status" in dependencies_report else 0
    evidence_count = len(evidence_report)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Readiness areas assessed", f"{assessed_count} / {total_areas}")
    m2.metric("Evidence found — review needed", review_needed_count, help="Evidence has been identified, but has not yet been judged sufficient to support the readiness conclusion.")
    m3.metric("Supported by evidence", supported_count, help="Only areas explicitly assessed as Supported by evidence are counted here.")
    m4.metric("Confirmed gaps", confirmed_gap_count)
    m5.metric("Open actions", open_action_count)
    st.caption(
        f"Other assessment statuses: {partially_supported_count} partially supported; "
        f"{conflicting_count} with conflicting evidence. ‘Evidence found — review needed’ is not counted as ‘Supported by evidence’."
    )

    st.caption(
        f"Additional records: {evidence_count} evidence-register rows; "
        f"{dependency_open_count} dependencies not marked complete/not applicable; "
        f"{blocked_action_count} actions blocked or waiting on prerequisites."
    )
    st.warning(
        "Interpretation rule: Not assessed means information has not yet been evaluated; "
        "it is not a confirmed gap. Counts are based on saved statuses and do not represent "
        "a certified readiness score or automatic go/no-go decision."
    )

    st.divider()
    st.subheader("1. Readiness profile")
    if readiness_report.empty:
        st.info("No readiness profile records found yet.")
    else:
        readiness_columns = [c for c in READINESS_COLUMNS if c in readiness_report.columns]
        st.dataframe(readiness_report[readiness_columns], use_container_width=True, hide_index=True)

    st.subheader("2. Evidence and traceability")
    if evidence_report.empty:
        st.info("No Research Evidence Register records found. Add evidence in the Evidence Register tab when available.")
    else:
        st.dataframe(evidence_report, use_container_width=True, hide_index=True)

    st.subheader("3. Deployment dependencies")
    if dependencies_report.empty:
        st.info("No deployment dependencies have been recorded yet.")
    else:
        st.dataframe(dependencies_report, use_container_width=True, hide_index=True)

    st.subheader("4. Actions and handover")
    if actions_report.empty:
        st.info("No actions have been recorded yet.")
    else:
        st.dataframe(actions_report, use_container_width=True, hide_index=True)

    st.subheader("5. Research questions")
    if research_report.empty:
        st.info("No research questions have been recorded yet.")
    else:
        st.dataframe(research_report, use_container_width=True, hide_index=True)

    # Build a plain-text report that is readable outside the application.
    from datetime import date
    report_lines = [
        "INTERCEPTOR SCALEREADY — INTEGRATED READINESS REPORT",
        f"Generated on: {date.today().isoformat()}",
        "",
        "PURPOSE AND LIMITATIONS",
        "This report consolidates records saved in the Interceptor ScaleReady research prototype.",
        "It is not an official report from The Ocean Cleanup or UNDP and does not certify readiness.",
        "Unknown or not-assessed items must not be interpreted as confirmed deficiencies.",
        "Evidence found — review needed means a source has been identified but not yet judged sufficient to support the readiness conclusion. It is intentionally counted separately from Supported by evidence.",
        "",
        "SUMMARY",
        f"Readiness areas assessed: {assessed_count} of {total_areas}",
        f"Areas with evidence found — review needed: {review_needed_count}",
        f"Areas marked supported by evidence: {supported_count}",
        f"Areas partially supported: {partially_supported_count}",
        f"Areas with conflicting evidence: {conflicting_count}",
        f"Areas marked gap confirmed by evidence: {confirmed_gap_count}",
        f"Open actions: {open_action_count}",
        f"Blocked or waiting actions: {blocked_action_count}",
        f"Dependencies not marked complete/not applicable: {dependency_open_count}",
        f"Evidence-register rows: {evidence_count}",
        "",
    ]

    def append_section(lines, heading, frame):
        lines.append(heading)
        if frame.empty:
            lines.append("No records saved.")
        else:
            lines.append(frame.fillna("").to_string(index=False))
        lines.append("")

    append_section(report_lines, "READINESS PROFILE", readiness_report)
    append_section(report_lines, "RESEARCH EVIDENCE REGISTER", evidence_report)
    append_section(report_lines, "DEPLOYMENT DEPENDENCIES", dependencies_report)
    append_section(report_lines, "ACTIONS AND HANDOVER", actions_report)
    append_section(report_lines, "RESEARCH QUESTIONS", research_report)
    report_text = "\n".join(report_lines)

    st.divider()
    st.subheader("Export report and supporting data")
    st.download_button(
        "Download integrated report (TXT)",
        data=report_text.encode("utf-8"),
        file_name="interceptor_scaleready_integrated_readiness_report.txt",
        mime="text/plain",
        key="download_integrated_readiness_report_v13",
    )

    export_frames = {
        "Readiness profile": (readiness_report, "interceptor_scaleready_readiness_profile.csv"),
        "Research evidence register": (evidence_report, "interceptor_scaleready_evidence_register.csv"),
        "Deployment dependencies": (dependencies_report, "interceptor_scaleready_dependencies.csv"),
        "Actions and handover": (actions_report, "interceptor_scaleready_actions.csv"),
        "Research questions": (research_report, "interceptor_scaleready_research_questions.csv"),
    }
    export_choice = st.selectbox("Choose a supporting CSV export", list(export_frames.keys()), key="report_csv_choice_v13")
    selected_frame, selected_filename = export_frames[export_choice]
    st.download_button(
        f"Download {export_choice} CSV",
        data=selected_frame.to_csv(index=False).encode("utf-8"),
        file_name=selected_filename,
        mime="text/csv",
        key="download_report_supporting_csv_v13",
    )
    st.caption(
        "The integrated report is generated from current saved CSV records. Review source quality, "
        "ownership, and uncertainty before using it to support a real deployment decision."
    )
