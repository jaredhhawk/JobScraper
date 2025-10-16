# JobScraper Epics and Stories

This document captures the product development backlog for JobScraper across multiple epics. Each epic is listed with its goal, stories, and acceptance criteria.

## Epic 1: Lead Discovery
**Goal:** Continuously surface relevant opportunities in the target industry (e.g., PropTech, ClimateTech, FinTech).

### Story 1.1: Deep searches into target-industry startups with official postings
**Persona Goal:** As a persona, I want to do deep searches into target-industry startups that have official postings so I can reach out and apply.

**Acceptance Criteria:**
- Job sources (e.g., BuiltIn, Otta, Greenhouse) configurable per industry profile.
- System fetches postings at least once per day.
- Only roles matching my location filter (Seattle / Remote / Hybrid) are returned.
- Industry profile defines search tags and sources.

### Story 1.2: Surface likely-hiring companies without official postings
**Persona Goal:** As a persona, I want to find companies in my target industry that may not have official postings but are likely hiring people with my experience so I can do tailored outreach.

**Acceptance Criteria:**
- “Likely hiring” flagged by signals (funding, headcount growth, exec hires).
- Signal thresholds customizable per industry profile.
- Each lead includes company name, website, and contacts.
- Leads stored in Notion DB.

### Story 1.3: Improve unposted job discovery methods
**Persona Goal:** As a persona, I want to continually improve my methods of finding unposted potential jobs across industries so I increase my odds of employment.

**Acceptance Criteria:**
- Feedback loop to mark leads as “useful” or “not useful.”
- Improvements logged per industry profile.
- Adjustments applied to next lead batch.

### Story 1.4: Honor preferred geography and remote options
**Persona Goal:** As a persona, I only want leads that are either remote or in my preferred geography so I don’t waste time.

**Acceptance Criteria:**
- Location filter auto-applied at ingestion.
- Remote roles flagged separately.
- Leads outside preferred area excluded.

## Epic 2: Lead Management
**Goal:** Store, track, and avoid duplicate work on leads across industries.

### Story 2.1: Centralize leads in Notion DB
**Persona Goal:** As a persona, I want to store all leads in a Notion DB tagged by industry and source so I can manage them centrally.

**Acceptance Criteria:**
- Each lead includes industry tag.
- DB supports filtering by industry, urgency, score.
- Leads have unique IDs and deduplication logic cross-industry.

### Story 2.2: Prevent duplicate reviews of opportunities
**Persona Goal:** As a persona, I don’t want to review the same opportunities multiple times across domains so I can be efficient.

**Acceptance Criteria:**
- Duplicate detection runs across industry tags.
- Rejected leads don’t resurface unless criteria change.

## Epic 3: Lead Prioritization
**Goal:** Know where to focus effort for maximum ROI across industries.

### Story 3.1: Display urgency of each lead
**Persona Goal:** As a persona, I want to know the urgency of each lead regardless of industry.

**Acceptance Criteria:**
- Urgency based on posting age, funding recency, exec activity.
- Domain-specific adjustments from industry profile (e.g., faster cycles in SaaS).

### Story 3.2: Prioritize by skills, level, and industry match
**Persona Goal:** As a persona, I want to prioritize leads based on skills match, level match, and industry relevance so I can spend time wisely.

**Acceptance Criteria:**
- Resume parsed for skills vs job description.
- Skills match % and level match % calculated.
- Industry relevance score added to weighting formula.
- Leads auto-sorted by overall score.

## Epic 4: Workflow Guidance
**Goal:** Know exactly what to do for each lead.

### Story 4.1: Surface next steps per lead
**Persona Goal:** As a persona, I want to see next steps for any lead so I can be efficient.

**Acceptance Criteria:**
- “Next Step” field (e.g., Apply, Research, Reach Out).
- Auto-updates from status changes.
- Steps link to templates or contacts.
- Domain-specific tips appear via industry context.

### Story 4.2: Provide semi-automated workflows
**Persona Goal:** As a persona, I don’t want everything fully automated so I keep control while saving time.

**Acceptance Criteria:**
- Manual review queue before outreach.
- Templates generated but not auto-sent.
- Automation toggle per task.

## Epic 5: Market Intelligence & Company Research
**Goal:** Turn raw leads into actionable insights per industry.

### Story 5.1: Show funding and growth signals
**Persona Goal:** As a persona, I want funding and growth signals so I can detect companies likely hiring.

**Acceptance Criteria:**
- Ingest funding, headcount, office expansions from industry-specific APIs.
- Signals shown with each lead.
- Urgency score updates automatically.

### Story 5.2: Provide competitor and peer benchmarking
**Persona Goal:** As a persona, I want competitor and peer benchmarking so I can refine targets.

**Acceptance Criteria:**
- Peer companies in same sector auto-listed.
- Benchmarks include hiring patterns.
- “Who’s hiring in my space” dashboard filtered by industry.

### Story 5.3: Highlight trigger events for outreach timing
**Persona Goal:** As a persona, I want to surface trigger events so I can time outreach.

**Acceptance Criteria:**
- Event types include exec hires, partnerships, acquisitions, launches.
- Events tie to company profiles and send notifications.

## Epic 6: Networking & Warm Introductions
**Goal:** Increase outreach effectiveness across industries.

### Story 6.1: Identify mutual LinkedIn connections
**Acceptance Criteria:** LinkedIn API/CSV checked vs lead list; “warm intro available” tag applied.

### Story 6.2: Generate industry-specific connection lists
**Acceptance Criteria:** Cross-reference company with school, employer, or VC portfolio data.

### Story 6.3: Provide tailored outreach templates
**Acceptance Criteria:** Templates vary by persona and industry context; user can edit before sending.

## Epic 7: Resume & Skill Alignment
**Goal:** Tailor applications to each industry for higher interview rates.

### Story 7.1: Highlight top resume bullets per lead
**Acceptance Criteria:** Resume parsed; job description mapped; top three bullets shown in Notion.

### Story 7.2: Show skill gap analysis
**Acceptance Criteria:** Job description keywords vs resume keywords compared; missing skills highlighted; suggested phrasing added; domain vocabulary map bridges synonyms across industries.

### Story 7.3: Auto-generate targeted outreach drafts
**Acceptance Criteria:** Draft outreach messages pull from resume and job description; industry language applied.

## Epic 8: Productivity & Time Management
**Goal:** Stay organized and consistent across multiple industries.

### Story 8.1: Rank leads by effort vs potential payoff
**Acceptance Criteria:** Effort and payoff estimated; matrix displayed per industry.

### Story 8.2: Deliver periodic lead summaries
**Acceptance Criteria:** Daily/weekly digest includes industry breakdown and reminders.

### Story 8.3: Provide follow-up reminders
**Acceptance Criteria:** Reminder dates and alerts tracked in Notion and email.

## Epic 9: Feedback & Continuous Improvement
**Goal:** Refine system accuracy and strategy per industry.

### Story 9.1: Capture lead fit feedback
**Acceptance Criteria:** Feedback field enables marking leads as “good” or “bad” fit; model learns preferences per industry.

### Story 9.2: Track conversion funnel metrics
**Acceptance Criteria:** Funnel metrics tracked per industry and in aggregate (Leads → Applied → Interview → Offer).

### Story 9.3: Recommend new sources or tactics
**Acceptance Criteria:** System monitors conversion rates; suggests better boards, approaches, or resume tweaks when performance dips.

## Epic 10: Risk & Compliance
**Goal:** Ensure safe and compliant data use for all domains.

### Story 10.1: Respect scraping rules and API terms
**Acceptance Criteria:** Intervals and volume documented; alerts triggered for potential violations.

### Story 10.2: Provide clear source attribution
**Acceptance Criteria:** Source and timestamp required for each lead; visible in Notion DB; domain-specific data licenses honored (e.g., MLS, financial data).

## Epic 11: Analytics & Insights
**Goal:** Surface patterns and performance metrics across industries.

### Story 11.1: Visualize job search funnel
**Acceptance Criteria:** Dashboard auto-updates from lead statuses; charts show trends per industry.

### Story 11.2: Highlight highest-ROI sources by industry
**Acceptance Criteria:** Conversion rates computed by source; top performers highlighted.

### Story 11.3: Measure time-to-action
**Acceptance Criteria:** Timestamps tracked; averages shown by industry for discovery-to-outreach cycle.

### Story 11.4: Track outreach response rates
**Acceptance Criteria:** Outreach attempts logged; response types captured; charts available by channel and industry.

### Story 11.5: Provide insight-driven recommendations
**Acceptance Criteria:** Analytics flag weak points (e.g., low interview conversion in PropTech); suggests tactics; weekly refresh generated.

## Epic 12: Industry Profiles (New)
**Goal:** Define and manage industry-specific settings for a flexible, cross-domain job-search system.

### Story 12.1: Create and save multiple industry profiles
**Acceptance Criteria:** Profiles include source list, keyword set, signal thresholds, and weighting rules.

### Story 12.2: Toggle or merge profiles to expand search scope
**Acceptance Criteria:** Switching updates queries and views in real time.

### Story 12.3: Clone profiles to test variations
**Acceptance Criteria:** Profiles editable and versioned.

### Story 12.4: Ensure analytics respect active profile filters
**Acceptance Criteria:** All reports reflect current profile selection and enable comparisons between profiles.
