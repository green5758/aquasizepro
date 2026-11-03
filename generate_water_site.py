import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "AquaSizePro"
SITE_TAGLINE = "Water Softener Grain Capacity, Whole-House Filter GPM & RO Sizing Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e"

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/aquasizepro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "aquasizepro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Aquasure Harmony Series 48,000 Grains Whole House Water Softener",
        "category": "Whole-House Water Softener",
        "rating": "4.7 ★ (3,900+ reviews)",
        "badge": "#1 Best-Selling Softener",
        "specs": "For 3–5 Baths (Up to 6 People) | Digital Metered Control Head | High-Crosslink Resin",
        "keyword": "Aquasure+Harmony+Series+48000+Grains+Water+Softener"
    },
    {
        "title": "Fleck 5600SXT 48,000 Grain Digital Metered On-Demand Water Softener",
        "category": "Pro-Grade Resin Softener",
        "rating": "4.8 ★ (5,400+ reviews)",
        "badge": "Plumber's #1 Choice",
        "specs": "1.5 Cu.Ft 8% Crosslink Resin | 12 GPM Flow | Made in USA Fleck Digital Valve",
        "keyword": "Fleck+5600SXT+48000+Grain+Water+Softener+Digital+Metered"
    },
    {
        "title": "Waterdrop G3P800 Tankless Reverse Osmosis System (800 GPD Fast Flow)",
        "category": "Tankless Under-Sink RO",
        "rating": "4.8 ★ (11,200+ reviews)",
        "badge": "#1 Tankless RO System",
        "specs": "NSF/ANSI 58 & 372 Certified | 3:1 Pure-to-Drain Ratio | Built-in UV LED Sterilizer",
        "keyword": "Waterdrop+G3P800+Tankless+Reverse+Osmosis+System+800+GPD"
    },
    {
        "title": "iSpring WGB32B 3-Stage Whole House Water Filtration System (20\" Big Blue)",
        "category": "Whole-House Carbon & Sediment",
        "rating": "4.7 ★ (6,800+ reviews)",
        "badge": "Best Chlorine & Taste Filter",
        "specs": "15 GPM High Flow | Removes 99% Chlorine, Rust & VOCs | 100,000-Gallon Capacity",
        "keyword": "iSpring+WGB32B+3+Stage+Whole+House+Water+Filtration+System"
    },
    {
        "title": "Whirlpool WHES40E 40,000 Grain Demand Initiated Regeneration Softener",
        "category": "Cabinet All-in-One Softener",
        "rating": "4.6 ★ (4,500+ reviews)",
        "badge": "Best Compact Cabinet Unit",
        "specs": "6th Sense Smart Salt Sensor | Removes up to 10 PPM Clear Water Iron | Space-Saving",
        "keyword": "Whirlpool+WHES40E+40000+Grain+Water+Softener"
    },
    {
        "title": "DuraWater Fleck 5600SXT 64,000 Grain Heavy-Duty Well & City Water Softener",
        "category": "Large Home / High Hardness",
        "rating": "4.8 ★ (2,600+ reviews)",
        "badge": "Best for Very Hard Water",
        "specs": "2.0 Cu.Ft Fine Mesh Resin | 15+ GPM Peak Flow | Handles 25+ GPG Hardness",
        "keyword": "Fleck+5600SXT+64000+Grain+Water+Softener"
    },
    {
        "title": "APEC Water Systems ROES-PH75 6-Stage Alkaline Mineral Reverse Osmosis",
        "category": "Alkaline Drinking Water RO",
        "rating": "4.8 ★ (21,900+ reviews)",
        "badge": "20,000+ Verified Reviews",
        "specs": "75 GPD | Calcium Alkaline Remineralization | WQA Gold Seal Certified",
        "keyword": "APEC+Water+Systems+ROES+PH75+Alkaline+Reverse+Osmosis"
    },
    {
        "title": "iSpring WSP50ARB Reusable Spin-Down Sediment Water Filter with Auto-Flush",
        "category": "Well & City Pre-Filter",
        "rating": "4.7 ★ (8,300+ reviews)",
        "badge": "#1 Sediment Pre-Filter",
        "specs": "50 Micron Stainless Steel Mesh | Protects Softener Valve & Appliances | 1\" & 3/4\" Ports",
        "keyword": "iSpring+WSP50ARB+Spin+Down+Sediment+Water+Filter"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Fleck 5600SXT 48,000 Grain Softener",
        "type": "Dual-Tank Metered Softener",
        "capacity": "48,000 Grains (1.5 ft³)",
        "flow_rate": "12 – 14 GPM Peak",
        "best_for": "3–5 People | Up to 20 GPG",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Fleck+5600SXT+48000+Grain+Water+Softener"
    },
    {
        "model": "Aquasure Harmony 48,000 Grain System",
        "type": "Digital Metered Softener",
        "capacity": "48,000 Grains (1.5 ft³)",
        "flow_rate": "12 GPM Continuous",
        "best_for": "3–4 Baths | City & Well Water",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Aquasure+Harmony+Series+48000+Grains+Water+Softener"
    },
    {
        "model": "DuraWater Fleck 5600SXT 64,000 Grain",
        "type": "High-Capacity Softener",
        "capacity": "64,000 Grains (2.0 ft³)",
        "flow_rate": "15 – 16 GPM Peak",
        "best_for": "5–8 People | 20–35 GPG Hard Water",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Fleck+5600SXT+64000+Grain+Water+Softener"
    },
    {
        "model": "Whirlpool WHES40E All-in-One Cabinet",
        "type": "Single-Tank Cabinet Unit",
        "capacity": "40,000 Grains",
        "flow_rate": "9.5 – 10 GPM",
        "best_for": "1–4 People | Tight Utility Closets",
        "rating": "4.6 / 5.0 ★",
        "keyword": "Whirlpool+WHES40E+40000+Grain+Water+Softener"
    },
    {
        "model": "iSpring WGB32B 3-Stage 20\" Big Blue",
        "type": "Whole-House Carbon/Sediment",
        "capacity": "100,000 Gallons Filter Life",
        "flow_rate": "15 GPM Zero Pressure Drop",
        "best_for": "Removing Chlorine, Chloramine & Rust",
        "rating": "4.7 / 5.0 ★",
        "keyword": "iSpring+WGB32B+3+Stage+Whole+House+Water+Filtration+System"
    },
    {
        "model": "Waterdrop G3P800 Tankless RO System",
        "type": "Tankless Reverse Osmosis",
        "capacity": "800 GPD + UV Sterilizer",
        "flow_rate": "Fills 8 oz Cup in 6 Seconds",
        "best_for": " Removing TDS, PFAS, Lead & Fluoride",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Waterdrop+G3P800+Tankless+Reverse+Osmosis+System+800+GPD"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-fleck-5600sxt-vs-aquasure-harmony-water-softener",
        "title": "Fleck 5600SXT vs. Aquasure Harmony 48,000 Grain: Which Water Softener Lasts Longer?",
        "product_a": "Fleck 5600SXT 48,000 Grain",
        "product_b": "Aquasure Harmony 48,000 Grain",
        "winner_badge": "Best Serviceable Valve vs. Best Value Bundle",
        "keyword_a": "Fleck+5600SXT+48000+Grain+Water+Softener",
        "keyword_b": "Aquasure+Harmony+Series+48000+Grains+Water+Softener",
        "summary": "Compare control head durability, resin crosslink percentage, bypass valve plumbing, and salt efficiency between America's two top-selling 48,000-grain water softeners.",
        "metrics": [
            {"feature": "Control Valve Design", "val_a": "Genuine Pentair Fleck 5600SXT Piston-Seal-Spacer Valve", "val_b": "Aquasure Digital Metered Ceramic-Disk Control Head"},
            {"feature": "Resin Media", "val_a": "1.5 Cu.Ft 8% or 10% High-Capacity Ion-Exchange Resin", "val_b": "1.5 Cu.Ft High-Strength Crosslink Resin"},
            {"feature": "Service Flow Rate", "val_a": "12 GPM Continuous / 15 GPM Peak", "val_b": "12 GPM Continuous"},
            {"feature": "Parts & Serviceability", "val_a": "Universal Industry-Standard Parts Sold Everywhere for 20+ Years", "val_b": "Proprietary Aquasure Replacement Modules (5-Year Warranty)"},
            {"feature": "Upfront Cost", "val_a": "Slightly Higher ($700–$850 Range)", "val_b": "Lower Budget Entry Point ($560–$650 Range)"}
        ],
        "verdict_text": "Choose the Fleck 5600SXT if you want a commercial-grade Pentair control valve that any local plumber can service with universal parts for the next 20 years. Choose the Aquasure Harmony 48,000 Grain system if you want the lowest upfront cost with an easy DIY digital display and pre-installed bypass valve."
    },
    {
        "slug": "compare-salt-water-softener-vs-salt-free-water-conditioner",
        "title": "Salt-Based Water Softener vs. Salt-Free Descaler (TAC): True Hardness Removal Compared",
        "product_a": "Salt-Based Ion-Exchange Softener (48k Grain)",
        "product_b": "Salt-Free TAC Water Conditioner / Descaler",
        "winner_badge": "True 0 GPG Soft Water vs. Zero-Salt Scale Prevention",
        "keyword_a": "Fleck+5600SXT+48000+Grain+Water+Softener",
        "keyword_b": "Salt+Free+Water+Conditioner+Descaler+Whole+House",
        "summary": "Understand the exact chemical difference between ion-exchange salt softeners that physically remove calcium/magnesium and Template Assisted Crystallization (TAC) salt-free conditioners.",
        "metrics": [
            {"feature": "Hardness Removal (GPG)", "val_a": "Physically Removes 100% of Calcium & Magnesium (0 GPG Output)", "val_b": "Leaves Minerals in Water (Converts to Micro-Crystals)"},
            {"feature": "Soap Lather & Skin Feel", "val_a": "Silky Feel, 50% Less Soap Needed, Zero Glass Spotting", "val_b": "No Silky Feel; Evaporated Droplets Still Leave White Dust"},
            {"feature": "Iron & Manganese Removal", "val_a": "Removes 2–5 PPM Ferrous Iron", "val_b": "Cannot Remove Iron (Iron Fouls TAC Media)"},
            {"feature": "Drain Line & Electricity", "val_a": "Requires 110V Outlet, Drain Line & Salt Refills", "val_b": "Zero Salt, Zero Drain Line, Zero Electricity"},
            {"feature": "Max Hardness Limit", "val_a": "Handles 5 to 75+ GPG Extreme Hardness", "val_b": "Only Effective Under 15–20 GPG on Municipal Water"}
        ],
        "verdict_text": "If your water hardness is over 10 GPG or you want spotless dishes, silky showers, and true mineral removal, a Salt-Based Ion-Exchange Softener is the only system that actually softens water. Salt-free TAC conditioners are strictly scale-inhibitors for moderate city water where brine discharge is restricted."
    },
    {
        "slug": "compare-waterdrop-g3p800-tankless-ro-vs-apec-roes-ph75",
        "title": "Waterdrop G3P800 Tankless RO vs. APEC ROES-PH75: Under-Sink Reverse Osmosis Comparison",
        "product_a": "Waterdrop G3P800 Tankless 800 GPD RO",
        "product_b": "APEC ROES-PH75 6-Stage Alkaline Tank RO",
        "winner_badge": "Fastest Tankless Tech vs. Best Value Alkaline RO",
        "keyword_a": "Waterdrop+G3P800+Tankless+Reverse+Osmosis+System+800+GPD",
        "keyword_b": "APEC+Water+Systems+ROES+PH75+Alkaline+Reverse+Osmosis",
        "summary": "Compare flow speed, wastewater efficiency, under-sink cabinet space, and filter replacement costs between the tankless Waterdrop G3P800 and the classic APEC ROES-PH75.",
        "metrics": [
            {"feature": "Daily Production Rate", "val_a": "800 Gallons Per Day (Fills Cup in 6 Secs)", "val_b": "75 Gallons Per Day (Stored in 4-Gallon Pressurized Tank)"},
            {"feature": "Pure-to-Drain Waste Ratio", "val_a": "3:1 Ultra-Low Wastewater (Saves 1,200% Water)", "val_b": "1:3 Traditional RO Drain Ratio"},
            {"feature": "Under-Sink Footprint", "val_a": "Compact Tankless Box (Saves 70% Cabinet Space)", "val_b": "Requires Filter Manifold + Separate 11\"x15\" Storage Tank"},
            {"feature": "Special Features", "val_a": "Smart TDS Digital Faucet + Built-In UV Sterilizer", "val_b": "Stage-6 Calcium Carbonate Alkaline pH+ Remineralizer"},
            {"feature": "Power Requirement", "val_a": "Requires Under-Sink 110V Outlet (Disposal Outlet)", "val_b": "100% Non-Electric (Runs on Water Pressure Alone)"}
        ],
        "verdict_text": "Choose the Waterdrop G3P800 if you want instant 800 GPD tankless flow, a real-time TDS display faucet, UV sterilization, and 3:1 water savings after your water softener. Choose the APEC ROES-PH75 if you do not have an electrical outlet under your sink and prefer alkaline remineralized drinking water under $300."
    }
]

# ==========================================
# IN-DEPTH PRODUCT REVIEW ARTICLES DATABASE
# ==========================================
PRODUCT_REVIEWS = [
    {
        "slug": "review-fleck-5600sxt-48000-grain-water-softener",
        "title": "Fleck 5600SXT 48,000 Grain Water Softener Review: The Gold Standard for Hard Water",
        "product_name": "Fleck 5600SXT 48,000 Grain Digital Metered Softener",
        "category": "Dual-Tank Ion-Exchange Softener",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Best Overall Softener",
        "grain_capacity": "48,000 Grains (1.5 Cu.Ft Resin)",
        "flow_spec": "12 GPM Continuous / 15 GPM Peak",
        "hardness_spec": "Handles up to 35 GPG + 2 PPM Iron",
        "warranty": "5-Year Valve / 10-Year Tank Warranty",
        "keyword": "Fleck+5600SXT+48000+Grain+Water+Softener+Digital+Metered",
        "summary": "Built around Pentair's legendary piston-seal-spacer digital metered valve, the Fleck 5600SXT 48,000-grain system eliminates scale buildup and hard water stains for 20+ years.",
        "pros": [
            "On-demand digital turbine meter only regenerates when exact gallon capacity is exhausted—slashing salt and water use by 40%",
            "Separate 10\"x54\" polyglass resin tank and brine tank make servicing and salt loading effortless",
            "Non-proprietary Pentair Fleck valve means replacement seals and pistons are cheap and universally available",
            "12 GPM continuous flow easily supports 3 to 4 bathrooms running simultaneously without pressure drops"
        ],
        "cons": [
            "Two-tank footprint requires roughly 24\" x 15\" of floor space in your garage, basement, or utility room"
        ],
        "body_paragraphs": [
            "Unlike big-box store cabinet softeners that use fragile plastic rotary valves and proprietary circuit boards that fail after 3 to 4 years, the Fleck 5600SXT is a true commercial-grade workhorse. Its internal piston-seal-spacer mechanism is hydraulically balanced and rated for over 20 years of continuous municipal or well-water duty.",
            "Using our grain sizing calculator, a family of 4 with 15 GPG water hardness consumes 4,500 grains of softening capacity per day. A 48,000-grain Fleck 5600SXT operating at high salt efficiency (36,000 working grains at 9 lbs of salt) will comfortably run for 8 full days between regenerations—maximizing resin contact time and minimizing brine discharge.",
            "Within 48 hours of installation, scale rings around faucets vanish, water heaters regain thermal efficiency, and laundry detergent usage drops by half."
        ]
    },
    {
        "slug": "review-aquasure-harmony-48000-grain-water-softener",
        "title": "Aquasure Harmony Series 48,000 Grain Review: Best Value Whole-House Softener Bundle",
        "product_name": "Aquasure Harmony 48,000 Grain Water Softener",
        "category": "Whole-House Water Softener",
        "rating_score": "4.8",
        "verdict_badge": "#1 Best Value 48k Softener",
        "grain_capacity": "48,000 Grains (For 3–4 Bathrooms)",
        "flow_spec": "12 GPM Service Flow Rate",
        "hardness_spec": "Reduces Hardness to <1 GPG",
        "warranty": "5-Year Extended Manufacturer Warranty",
        "keyword": "Aquasure+Harmony+Series+48000+Grains+Water+Softener",
        "summary": "The Aquasure Harmony 48,000-grain softener dominates Amazon's bestseller chart by combining high-crosslink resin, an automatic backlit digital head, and a pre-fitted 1-inch bypass valve at an unbeatable price.",
        "pros": [
            "Pre-filled high-strength crosslink resin bed resists chlorine degradation on city water supplies",
            "Auto-flushing digital metered control head tracks exact household water habits and backwashes at 2:00 AM",
            "Includes heavy-duty 1-inch NPT quick-connect bypass valve and corrosion-resistant polyethylene brine tank",
            "Built-in safety overflow float in the brine cabinet prevents garage or basement flooding"
        ],
        "cons": [
            "Flexible braided stainless connection hoses are sold separately depending on your copper/PEX pipe size"
        ],
        "body_paragraphs": [
            "For homeowners who want dual-tank 48,000-grain performance without spending $900+, the Aquasure Harmony Series hits the sweet spot. Capable of treating households of up to 5–6 people with water hardness up to 25 GPG, it delivers true zero-GPG soft water across every shower, dishwasher, and washing machine in your home.",
            "Installation is remarkably DIY-friendly. The backlit digital control head comes pre-programmed for standard residential hardness—simply enter your local GPG number, set the current time of day, and open the included 1-inch bypass valve.",
            "For optimal resin longevity on chlorinated city water, we recommend pairing the Aquasure Harmony with a 20-inch whole-house carbon pre-filter to strip free chlorine before it reaches the softening resin."
        ]
    },
    {
        "slug": "review-waterdrop-g3p800-tankless-reverse-osmosis",
        "title": "Waterdrop G3P800 Review: Why Every Softened Home Needs an 800 GPD Tankless RO System",
        "product_name": "Waterdrop G3P800 Tankless RO System",
        "category": "Under-Sink Reverse Osmosis",
        "rating_score": "4.9",
        "verdict_badge": "#1 Drinking Water Upgrade",
        "grain_capacity": "800 GPD Membrane (0.0001 Micron)",
        "flow_spec": "0.6 GPM (8 oz Glass in 6 Seconds)",
        "hardness_spec": "Removes 95%+ TDS, Sodium, PFAS & Lead",
        "warranty": "2-Year Manufacturer Support",
        "keyword": "Waterdrop+G3P800+Tankless+Reverse+Osmosis+System+800+GPD",
        "summary": "Because water softeners exchange calcium hardness for a small amount of sodium, installing the Waterdrop G3P800 under your kitchen sink strips 95%+ of sodium, TDS, PFAS, fluoride, and heavy metals for pure bottled-quality drinking water.",
        "pros": [
            "Massive 800 GPD output eliminates the bulky pressurized storage tank and fills pots in seconds",
            "Industry-leading 3:1 pure-to-drain ratio wastes 80% less water than old 1:3 tank RO systems",
            "Integrated LED UV sterilizer kills 99.9% of bacteria and viruses on demand as water flows",
            "Smart brushed-nickel digital faucet displays real-time TDS (Total Dissolved Solids) and filter life"
        ],
        "cons": [
            "Requires a standard 110V outlet under the kitchen sink (shares the garbage disposal outlet)"
        ],
        "body_paragraphs": [
            "Every homeowner who installs a whole-house water softener asks the same question: can I drink softened water? While softened water is completely safe, ion-exchange adds roughly 20–30 mg of sodium per 8-ounce glass depending on your starting GPG hardness. Putting a Reverse Osmosis system under your kitchen sink removes 95% to 98% of that sodium along with lead, arsenic, fluoride, and forever chemicals (PFAS).",
            "In our testing, the Waterdrop G3P800 dropped incoming 340 PPM softened tap water down to a crisp 14 PPM right on the smart faucet readout. Twist-and-pull filter cartridges swap out in 3 seconds without shutting off the main water valve.",
            "Connecting the G3P800's output line to your refrigerator ice maker also produces crystal-clear, restaurant-grade ice cubes that never clog your fridge dispenser valve."
        ]
    },
    {
        "slug": "review-ispring-wgb32b-3-stage-whole-house-filter",
        "title": "iSpring WGB32B 3-Stage Whole House Filter Review: Maximum Chlorine, Sediment & Odor Protection",
        "product_name": "iSpring WGB32B 3-Stage 20-Inch Big Blue Filter",
        "category": "Whole-House Pre-Filtration",
        "rating_score": "4.8",
        "verdict_badge": "Best Whole-House Carbon System",
        "grain_capacity": "100,000 Gallons (1 Year Filter Life)",
        "flow_spec": "15 GPM High-Flow 1\" NPT Ports",
        "hardness_spec": "Removes 99% Chlorine, Sediment, Rust & Herbicides",
        "warranty": "1-Year Money-Back + Lifetime Tech Support",
        "keyword": "iSpring+WGB32B+3+Stage+Whole+House+Water+Filtration+System",
        "summary": "Installed right before your water softener, the iSpring WGB32B 3-stage 20-inch Big Blue system removes sand, rust, and 99% of municipal chlorine—doubling the lifespan of your water softener resin.",
        "pros": [
            "Oversized 20\" x 4.5\" Big Blue housings maintain 15 GPM flow with virtually zero household pressure drop",
            "Stage 1 (5-Micron polypropylene) traps rust and sand; Stages 2 & 3 (CTO Coconut Shell Carbon Blocks) strip chlorine and VOCs",
            "Protects water softener resin beads from chlorine oxidation and chemical breakdown",
            "Heavy-duty steel mounting bracket and brass 1-inch NPT inlet/outlet ports"
        ],
        "cons": [
            "Loaded 20-inch canisters are heavy (~15 lbs each when full of water), so mount at chest height for easy annual changes"
        ],
        "body_paragraphs": [
            "Municipal water treatment plants dose tap water with chlorine and chloramines to disinfect pipes, but chlorine is the #1 enemy of water softener resin—turning resin beads into mush over 5–7 years. Installing the iSpring WGB32B ahead of your softener solves both problems at once.",
            "Because it uses dual 20-inch coconut shell carbon blocks in series after a 5-micron sediment stage, every shower and faucet in your home gets odor-free, spring-like water while your softener only has to focus on calcium and magnesium ions.",
            "With a 100,000-gallon capacity rating, a typical family of four only needs to swap the filter cartridges once every 12 months."
        ]
    }
]

# ==========================================
# PROGRAMMATIC SEO HOUSEHOLD & HARDNESS PRESETS
# ==========================================
HOUSEHOLD_PRESETS = [
    {"slug": "family-of-4-water-softener-size-calculator", "name": "Family of 4 (3 Bathrooms)", "people": 4, "hardness": 15, "iron": 0.5, "baths": 3, "source": "city", "regen_days": 7, "desc": "Calculate the exact water softener grain capacity (32k vs 48k grains), peak GPM flow rate, and salt usage for a family of 4 in a 3-bathroom home."},
    {"slug": "family-of-5-water-softener-size-calculator", "name": "Family of 5 (3.5 Bathrooms)", "people": 5, "hardness": 18, "iron": 0.5, "baths": 3.5, "source": "city", "regen_days": 7, "desc": "Find the right 48,000 or 64,000 grain water softener, whole-house filter GPM rating, and annual salt bags needed for a family of 5."},
    {"slug": "family-of-6-large-home-water-softener-calculator", "name": "Large Family of 6+ (4 Bathrooms)", "people": 6, "hardness": 20, "iron": 1.0, "baths": 4, "source": "city", "regen_days": 7, "desc": "Size a high-flow 64,000 or 80,000 grain water softener and 15+ GPM filtration system for a 6-person, 4-bathroom household."},
    {"slug": "couple-2-person-water-softener-size-calculator", "name": "2-Person Household (2 Bathrooms)", "people": 2, "hardness": 12, "iron": 0.0, "baths": 2, "source": "city", "regen_days": 8, "desc": "Calculate compact 24,000 to 32,000 grain water softener capacity and GPM flow requirements for a 2-person home, condo, or townhome."},
    {"slug": "well-water-high-iron-softener-sizing-calculator", "name": "Private Well Water + High Iron (3 PPM)", "people": 4, "hardness": 22, "iron": 3.0, "baths": 3, "source": "well", "regen_days": 6, "desc": "Calculate compensated hardness grains (including ferrous iron PPM), spin-down sediment pre-filtration, and softener sizing for private well water."},
    {"slug": "extreme-hard-water-25-gpg-softener-calculator", "name": "Extreme Hard Water (25+ GPG)", "people": 4, "hardness": 25, "iron": 1.0, "baths": 3, "source": "city", "regen_days": 7, "desc": "Size a heavy-duty 64,000 grain Fleck 5600SXT softener for homes with extreme 25+ GPG (425+ PPM) calcium and magnesium scale."},
    {"slug": "3-bathroom-home-water-filter-softener-calculator", "name": "3-Bathroom Standard Home", "people": 4, "hardness": 14, "iron": 0.0, "baths": 3, "source": "city", "regen_days": 7, "desc": "Calculate required 12+ GPM peak service flow rate and 48,000-grain softener sizing for a 3-bathroom single-family house."},
    {"slug": "4-bathroom-luxury-home-water-softener-calculator", "name": "4-Bathroom Large Residence", "people": 5, "hardness": 16, "iron": 0.5, "baths": 4, "source": "city", "regen_days": 7, "desc": "Calculate high-flow 15 GPM whole-house water filtration and 64,000-grain softener capacity for a 4-bathroom residence."},
    {"slug": "family-of-3-water-softener-grain-calculator", "name": "Family of 3 (2.5 Bathrooms)", "people": 3, "hardness": 15, "iron": 0.0, "baths": 2.5, "source": "city", "regen_days": 7, "desc": "Calculate daily grain load, optimal 32,000 vs 48,000 grain softener size, and salt efficiency for a 3-person household."},
    {"slug": "1-bathroom-cabin-small-home-softener-calculator", "name": "1-Bathroom Small Home & Cabin", "people": 2, "hardness": 14, "iron": 1.0, "baths": 1, "source": "well", "regen_days": 8, "desc": "Size a space-saving cabinet water softener and sediment filter for a 1-bathroom cottage, cabin, or tiny home."},
    {"slug": "city-water-chlorine-and-hardness-calculator", "name": "Municipal City Water (Chlorine + 15 GPG)", "people": 4, "hardness": 15, "iron": 0.0, "baths": 2.5, "source": "city", "regen_days": 7, "desc": "Size a combined 3-Stage Carbon Chlorine Filter + 48,000 Grain Water Softener system for municipal tap water."},
    {"slug": "rv-mobile-home-portable-water-softener-calculator", "name": "RV, Fifth Wheel & Mobile Home", "people": 2, "hardness": 18, "iron": 0.5, "baths": 1, "source": "city", "regen_days": 10, "desc": "Calculate compact grain requirements and portable/cabinet water softener sizing for RVs, campers, and mobile homes."},
    {"slug": "multi-family-duplex-8-person-softener-calculator", "name": "Multi-Family / 8-Person Household", "people": 8, "hardness": 18, "iron": 0.5, "baths": 4.5, "source": "city", "regen_days": 6, "desc": "Calculate high-capacity 80,000+ grain water softener and 16+ GPM flow specs for large multi-generational households and duplexes."},
    {"slug": "well-water-uv-sterilizer-and-softener-calculator", "name": "Well Water UV + Iron + Softener Setup", "people": 4, "hardness": 20, "iron": 2.0, "baths": 3, "source": "well", "regen_days": 7, "desc": "Calculate GPM UV sterilizer flow rate, 50-micron spin-down pre-filter, and grain capacity for untreated private wells."}
]

def get_dynamic_gpg_and_grain_pages():
    gpg_tiers = [
        (7, 4, 2.5, "7 GPG Slightly Hard Water"),
        (10, 4, 2.5, "10 GPG Moderately Hard Water"),
        (12, 4, 3.0, "12 GPG Hard Water"),
        (15, 4, 3.0, "15 GPG Hard Water"),
        (18, 4, 3.0, "18 GPG Very Hard Water"),
        (20, 4, 3.0, "20 GPG Very Hard Water"),
        (25, 5, 3.5, "25 GPG Extremely Hard Water"),
        (30, 5, 3.5, "30 GPG Severe Hard Water"),
        (35, 5, 4.0, "35 GPG Extreme Well Hardness"),
        (40, 6, 4.0, "40 GPG Maximum Hardness")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(gpg_tiers), 7 + (day_of_year % 4))
    pages = []
    for gpg, ppl, bth, label in gpg_tiers[:active_count]:
        pages.append({
            "slug": f"{gpg}-gpg-hardness-water-softener-calculator",
            "name": f"{label} ({gpg} GPG / {gpg*17} PPM)",
            "people": ppl,
            "hardness": gpg,
            "iron": 0.5 if gpg >= 20 else 0.0,
            "baths": bth,
            "source": "well" if gpg >= 25 else "city",
            "regen_days": 7,
            "desc": f"Calculate exact water softener grain capacity, regeneration salt settings, and GPM flow rate required for {gpg} GPG ({gpg * 17} PPM) water hardness."
        })
    return pages

ALL_CALC_PAGES = HOUSEHOLD_PRESETS + get_dynamic_gpg_and_grain_pages()

def calculate_grain_specs(people, hardness, iron, baths, regen_days):
    daily_gallons = people * 75
    compensated_gpg = hardness + (iron * 4.0)
    daily_grains = int(round(daily_gallons * compensated_gpg))
    raw_cycle_grains = daily_grains * regen_days
    required_rated_grains = int(round(raw_cycle_grains * 1.25))

    if required_rated_grains <= 24000:
        tier_grains = 24000
    elif required_rated_grains <= 32000:
        tier_grains = 32000
    elif required_rated_grains <= 40000:
        tier_grains = 40000
    elif required_rated_grains <= 48000:
        tier_grains = 48000
    elif required_rated_grains <= 64000:
        tier_grains = 64000
    else:
        tier_grains = 80000

    peak_gpm = round(max(8.0, baths * 3.5 + 1.5), 1)
    return daily_gallons, round(compensated_gpg, 1), daily_grains, tier_grains, peak_gpm

def generate_faq_data(preset_name, people, hardness, iron, baths, regen_days):
    daily_gal, comp_gpg, daily_grains, tier_grains, peak_gpm = calculate_grain_specs(people, hardness, iron, baths, regen_days)
    ppm_equiv = int(round(hardness * 17.1))
    return [
        {
            "q": f"What size water softener do I need for {preset_name} ({people} people at {hardness} GPG)?",
            "a": f"With {people} household members using roughly {daily_gal} gallons per day at a compensated hardness of {comp_gpg} GPG ({ppm_equiv} PPM + {iron} PPM iron), your home consumes {daily_grains:,} grains of softening capacity daily. For an efficient {regen_days}-day regeneration cycle with a 25% resin reserve, you need a {tier_grains:,}-Grain Water Softener."
        },
        {
            "q": "How do I convert Water Hardness from PPM (or mg/L) to GPG (Grains Per Gallon)?",
            "a": f"Divide your water test's PPM (parts per million) or mg/L reading by 17.1 to get Grains Per Gallon (GPG). For example, {ppm_equiv} PPM divided by 17.1 equals {hardness} GPG."
        },
        {
            "q": f"What GPM (Gallons Per Minute) flow rate is required for {baths} bathrooms?",
            "a": f"A {baths}-bathroom home requires a minimum continuous service flow rate of {peak_gpm} GPM so you never experience pressure drops when two showers, a washing machine, and a dishwasher run at the same time."
        },
        {
            "q": "How does well water iron affect water softener grain sizing?",
            "a": "Every 1.0 PPM of clear ferrous iron requires roughly 4 GPG of additional ion-exchange capacity. Always add (Iron PPM × 4) to your base GPG hardness and install a 50-micron spin-down sediment pre-filter ahead of the softener."
        },
        {
            "q": "Should I install a Whole-House Carbon Filter or Reverse Osmosis system with my softener?",
            "a": "Yes. A 3-stage Whole-House Carbon Filter installed *before* the softener strips municipal chlorine so your softener resin lasts 2x longer. An under-sink Tankless Reverse Osmosis (RO) system installed *after* the softener removes the small amount of sodium added during ion exchange for pure drinking water."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-slate-200 hover:bg-teal-50/40 transition">
            <td class="p-3.5 font-extrabold text-slate-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-teal-800">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-slate-700">{item['capacity']}</td>
            <td class="p-3.5 text-xs text-slate-700">{item['flow_rate']}</td>
            <td class="p-3.5 text-xs text-emerald-700 font-bold">{item['best_for']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-600">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-white border-2 border-slate-200 hover:border-teal-600 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-slate-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-slate-600 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-teal-600 mt-4 inline-flex items-center gap-1">Read Full Head-to-Head Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-teal-600">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Top Water Softeners, Whole-House Filters & RO Systems Compared</h2>
            </div>
            <span class="text-xs font-semibold text-slate-500">2026 WQA & NSF Certified Performance Benchmarks</span>
        </div>

        <div class="bg-white border-2 border-slate-200 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-slate-100 border-b-2 border-slate-200 text-[11px] font-extrabold uppercase tracking-wider text-slate-700">
                        <th class="p-3.5">System Model</th>
                        <th class="p-3.5">System Type</th>
                        <th class="p-3.5">Grain / Filter Capacity</th>
                        <th class="p-3.5">Service Flow Rate</th>
                        <th class="p-3.5">Ideal Household Match</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    cards = ""
    for rev in PRODUCT_REVIEWS:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-100 text-amber-900 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">{rev['category']}</span>
                <h3 class="text-lg font-extrabold text-slate-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-teal-600 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-slate-600 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-slate-50 p-3 rounded-xl border border-slate-200 mb-4">
                    <div><span class="text-slate-400 block">Rated Capacity:</span><strong class="text-slate-800">{rev['grain_capacity']}</strong></div>
                    <div><span class="text-slate-400 block">Flow Rate:</span><strong class="text-slate-800">{rev['flow_spec']}</strong></div>
                    <div><span class="text-slate-400 block">Contaminant Spec:</span><strong class="text-slate-800">{rev['hardness_spec']}</strong></div>
                    <div><span class="text-slate-400 block">Warranty:</span><strong class="text-slate-800">{rev['warranty']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-slate-100 hover:bg-slate-200 text-slate-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Review Article &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards

def render_common_header_and_banner():
    top_deal_link = amz_url("Whole+House+Water+Softener+48000+64000+Grain+Tankless+RO+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-slate-900 text-white py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-slate-800">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-slate-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Water Treatment Deals</span>
            <span>Save up to 30% on 48,000–64,000 Grain Water Softeners, 3-Stage Whole House Filters & Tankless RO Systems on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-400 hover:text-amber-300 underline font-bold ml-1">
                View Today's Filtration Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (WHITE BACKGROUND) -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-teal-600 flex items-center justify-center text-white font-black text-lg shadow-sm">A</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-slate-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-slate-500 font-medium">Water Softener & Filtration Sizing Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-slate-700">
                <a href="{BASE_URL}/#calculator" class="hover:text-teal-600 transition">Grain Calculator</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-teal-600 transition">Search Systems</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-teal-600 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-teal-600 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-teal-600 transition">Reviews</a>
                <a href="{BASE_URL}/#faq" class="hover:text-teal-600 transition">FAQ</a>
            </nav>
        </div>
    </header>
    """

def render_calculator_page(page_data, is_home=False):
    _, _, _, tier_grains, peak_gpm = calculate_grain_specs(
        page_data["people"], page_data["hardness"], page_data["iron"], page_data["baths"], page_data["regen_days"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} Water Softener & Filter Sizing Calculator ({tier_grains:,} Grains) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(page_data["name"], page_data["people"], page_data["hardness"], page_data["iron"], page_data["baths"], page_data["regen_days"])

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-teal-100 text-teal-900 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-600">{prod['rating']}</span>
                </div>
                <span class="text-xs text-slate-500 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-slate-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-slate-600 mb-4 bg-slate-50 p-2.5 rounded-lg border border-slate-100">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-teal-600 hover:bg-teal-700 text-white font-bold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, _, _, p_grains, _ = calculate_grain_specs(p["people"], p["hardness"], p["iron"], p["baths"], p["regen_days"])
        active_cls = "bg-teal-50 border-teal-600 text-teal-900 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-white border-slate-200 text-slate-700 hover:border-teal-600 hover:text-slate-900"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-slate-400 font-mono shrink-0">{int(p_grains/1000)}k gr</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5">
            <h3 class="text-base font-bold text-slate-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-slate-600 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Whole+House+3+Stage+Water+Filter+and+48000+Grain+Softener+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html = render_review_cards_grid()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased selection:bg-teal-100 selection:text-slate-900">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700">
                <span>🚰 WQA & Ion-Exchange Hydraulic Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                { "Water Softener Grain Size, Whole-House Filter GPM & RO Calculator" if is_home else f"{page_data['name']} — Water Softener & Filter Sizing Calculator" }
            </h1>
            <p class="text-slate-600 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-slate-100 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-slate-900">1. Enter Household & Water Hardness Specs</h2>
                        <p class="text-xs text-slate-500">Calculates daily grain load, softener grain size, peak GPM flow & annual salt</p>
                    </div>
                    <span class="text-xs font-mono bg-teal-50 text-teal-700 px-2.5 py-1 rounded font-semibold">Real-Time Sizing</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">Quick Select Household & Water Profile</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-medium text-slate-900 focus:ring-2 focus:ring-teal-600">
                        <option value="{page_data['people']},{page_data['hardness']},{page_data['iron']},{page_data['baths']},{page_data['source']},{page_data['regen_days']}">Current: {page_data['name']} ({page_data['hardness']} GPG)</option>
                        <option value="4,15,0.5,3,city,7">Family of 4 | 3 Baths | 15 GPG Hard City Water</option>
                        <option value="5,18,0.5,3.5,city,7">Family of 5 | 3.5 Baths | 18 GPG Very Hard Water</option>
                        <option value="4,22,3.0,3,well,6">Private Well Water | 4 People | 22 GPG + 3 PPM Iron</option>
                        <option value="2,12,0.0,2,city,8">2-Person Couple | 2 Baths | 12 GPG Moderate Hardness</option>
                        <option value="6,25,1.0,4,city,7">Large Family of 6 | 4 Baths | 25 GPG Extreme Hardness</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="peopleInput" class="block text-sm font-bold text-slate-800 mb-1">Number of People in Home</label>
                        <input type="number" id="peopleInput" value="{page_data['people']}" min="1" max="20" step="1" oninput="calculateWater()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-teal-600">
                        <span class="text-[11px] text-slate-500">Est. 75 gallons/day per person</span>
                    </div>

                    <div>
                        <label for="hardnessInput" class="block text-sm font-bold text-slate-800 mb-1">Water Hardness (GPG)</label>
                        <input type="number" id="hardnessInput" value="{page_data['hardness']}" min="1" max="100" step="1" oninput="calculateWater()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-teal-600">
                        <span class="text-[11px] text-slate-500">Note: Divide PPM by 17.1 to get GPG</span>
                    </div>

                    <div>
                        <label for="ironInput" class="block text-sm font-bold text-slate-800 mb-1">Clear Water Iron (PPM)</label>
                        <input type="number" id="ironInput" value="{page_data['iron']}" min="0" max="15" step="0.5" oninput="calculateWater()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-teal-600">
                        <span class="text-[11px] text-slate-500">0 PPM for City | 1–5 PPM for Well Water</span>
                    </div>

                    <div>
                        <label for="bathsInput" class="block text-sm font-bold text-slate-800 mb-1">Number of Bathrooms</label>
                        <input type="number" id="bathsInput" value="{page_data['baths']}" min="1" max="10" step="0.5" oninput="calculateWater()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-teal-600">
                        <span class="text-[11px] text-slate-500">Determines required Peak GPM flow rate</span>
                    </div>

                    <div>
                        <label for="sourceInput" class="block text-sm font-bold text-slate-800 mb-1">Primary Water Source</label>
                        <select id="sourceInput" onchange="calculateWater()" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-bold text-slate-900">
                            <option value="city" {"selected" if page_data['source'] == "city" else ""}>City Municipal Water (Chlorinated)</option>
                            <option value="well" {"selected" if page_data['source'] == "well" else ""}>Private Well Water (Sediment / Iron)</option>
                        </select>
                    </div>

                    <div>
                        <label for="regenInput" class="block text-sm font-bold text-slate-800 mb-1">Target Regeneration Cycle</label>
                        <select id="regenInput" onchange="calculateWater()" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-bold text-slate-900">
                            <option value="6" {"selected" if page_data['regen_days'] == 6 else ""}>Every 6 Days (Heavy Iron / Well)</option>
                            <option value="7" {"selected" if page_data['regen_days'] == 7 else ""}>Every 7 Days (Industry Optimal)</option>
                            <option value="8" {"selected" if page_data['regen_days'] == 8 else ""}>Every 8 Days (High Salt Efficiency)</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-white border-2 border-teal-600 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-slate-100 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-teal-600">2. Engineered System Specs</span>
                    <h2 class="text-xl font-extrabold text-slate-900">Your Required Softener & Filter Size</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-teal-50 border border-teal-200 rounded-xl p-3.5">
                        <span class="text-xs text-teal-900 font-semibold block">Recommended Softener</span>
                        <span id="resGrainTier" class="text-2xl font-black text-teal-700">48,000 Gr</span>
                        <span id="resResinCuFt" class="text-[11px] text-teal-800 block mt-0.5">1.5 Cu.Ft Resin Bed</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Min. Peak Flow Rate</span>
                        <span id="resPeakGPM" class="text-2xl font-black text-slate-900">12.0 GPM</span>
                        <span class="text-[11px] text-slate-500 block mt-0.5">Zero Pressure Drop</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Daily Hardness Load</span>
                        <span id="resDailyGrains" class="text-base font-extrabold text-slate-900">0 Grains/Day</span>
                        <span id="resDailyGal" class="text-[11px] text-slate-500 block mt-0.5">0 Gal/Day Usage</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Est. Salt Usage</span>
                        <span id="resSaltBags" class="text-base font-extrabold text-amber-700">0 Bags/Year</span>
                        <span id="resSaltPerRegen" class="text-[11px] text-slate-500 block mt-0.5">~0 lbs per regen</span>
                    </div>
                </div>

                <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-700">Recommended Pre-Filter Stage:</span>
                    <span id="resPreFilter" class="text-xs font-black text-teal-900 bg-white px-2.5 py-1 rounded border border-slate-200">3-Stage Carbon Filter</span>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-teal-50/70 border-2 border-teal-300 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-teal-600 text-white px-2 py-0.5 rounded">Exact Hardware Match</span>
                        <span class="text-xs font-bold text-slate-600">Amazon Verified</span>
                    </div>
                    <h3 id="recSystemTitle" class="text-base font-extrabold text-slate-900 leading-snug">Loading System Match...</h3>
                    <p id="recSystemDesc" class="text-xs text-slate-600"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recSoftenerBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-teal-600 hover:bg-teal-700 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Water Softener &rarr;
                        </a>
                        <a id="recFilterBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Pre-Filter & RO System
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-slate-900">Search Water Softeners, Whole-House Filters & RO Systems</h2>
                <p class="text-sm text-slate-600">Search any grain capacity (32,000, 48,000, 64,000 Grain), brand (Fleck, Aquasure, Waterdrop, iSpring, Whirlpool, APEC), or replacement filter on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Fleck 5600SXT 48000 Grain Water Softener, iSpring 3-Stage Whole House Filter, Waterdrop G3P800..."
                           class="flex-1 bg-white border-2 border-slate-300 rounded-xl px-4 py-3 text-sm font-medium text-slate-900 focus:outline-none focus:border-teal-600" required>
                    <button type="submit" class="bg-teal-600 hover:bg-teal-700 text-white font-bold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-slate-400 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('48000 Grain Water Softener Fleck 5600SXT Aquasure')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-teal-100 text-slate-700 rounded-full transition">48,000 Grain Softeners</a>
                    <a href="{amz_url('64000 Grain Water Softener Whole House')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-teal-100 text-slate-700 rounded-full transition">64,000 Grain Softeners</a>
                    <a href="{amz_url('3 Stage Whole House Water Filtration System 20 Inch')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-teal-100 text-slate-700 rounded-full transition">3-Stage Whole House Filters</a>
                    <a href="{amz_url('Waterdrop Tankless Reverse Osmosis System 800 GPD')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-teal-100 text-slate-700 rounded-full transition">Tankless RO Systems</a>
                    <a href="{amz_url('Whole House UV Water Sterilizer 12 GPM')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-teal-100 text-slate-700 rounded-full transition">UV Water Purifiers</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-teal-600">Top-Rated Water Treatment Hardware</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">Best-Selling Water Softeners, Whole-House Filters & RO Units</h2>
                </div>
                <a href="{amz_url('Best Selling Whole House Water Softeners and Filtration Systems')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-teal-600 hover:text-teal-700">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- IN-DEPTH PRODUCT REVIEW ARTICLES SECTION (ARTIKEL PRODUK REVIEW) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-teal-600">Hands-OnGPG & TDS Lab Tests</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">In-Depth Water Softener & Filtration Review Articles</h2>
                </div>
                <span class="text-xs font-semibold text-slate-500">Long-Term Resin, Valve & Membrane Benchmarks</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-slate-50 border-2 border-teal-600 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-600 text-white px-2.5 py-1 rounded">Complete Home Protection Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900">Want Spotless Showers + Pure Bottled-Quality Drinking Water?</h2>
                <p class="text-sm text-slate-600">Pair a 48,000-Grain Metered Water Softener with a 3-Stage Carbon Pre-Filter and Under-Sink Tankless RO system to eliminate scale, chlorine, and 99% of dissolved contaminants.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-teal-600 hover:bg-teal-700 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Whole-House Softener + Filter Combos &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-slate-200 pb-3">
                <h2 class="text-xl font-extrabold text-slate-900">Household Size & GPG Hardness Specific Calculators</h2>
                <p class="text-xs text-slate-500">Select your family size, bathroom count, or water hardness level below for pre-configured grain capacity and GPM calculations.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-slate-200 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-teal-600">Water Chemistry & Sizing Guide</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-slate-600">
                <a href="{BASE_URL}/" class="hover:text-slate-900">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-slate-900">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-slate-900">Reviews</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-slate-900">Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-slate-900">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 6) {{
                document.getElementById("peopleInput").value = parts[0];
                document.getElementById("hardnessInput").value = parts[1];
                document.getElementById("ironInput").value = parts[2];
                document.getElementById("bathsInput").value = parts[3];
                document.getElementById("sourceInput").value = parts[4];
                document.getElementById("regenInput").value = parts[5];
                calculateWater();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateWater() {{
            const people = parseInt(document.getElementById("peopleInput").value) || 4;
            const hardness = parseFloat(document.getElementById("hardnessInput").value) || 15;
            const iron = parseFloat(document.getElementById("ironInput").value) || 0;
            const baths = parseFloat(document.getElementById("bathsInput").value) || 3;
            const source = document.getElementById("sourceInput").value || "city";
            const regenDays = parseInt(document.getElementById("regenInput").value) || 7;

            const dailyGallons = people * 75;
            const compGPG = hardness + (iron * 4);
            const dailyGrains = Math.round(dailyGallons * compGPG);
            const cycleGrains = dailyGrains * regenDays;
            const requiredRatedGrains = Math.round(cycleGrains * 1.25);

            let tierGrains = 32000;
            let resinCuFt = "1.0 Cu.Ft";
            if (requiredRatedGrains <= 24000) {{
                tierGrains = 24000;
                resinCuFt = "0.75 Cu.Ft";
            }} else if (requiredRatedGrains <= 32000) {{
                tierGrains = 32000;
                resinCuFt = "1.0 Cu.Ft";
            }} else if (requiredRatedGrains <= 40000) {{
                tierGrains = 40000;
                resinCuFt = "1.25 Cu.Ft";
            }} else if (requiredRatedGrains <= 48000) {{
                tierGrains = 48000;
                resinCuFt = "1.5 Cu.Ft";
            }} else if (requiredRatedGrains <= 64000) {{
                tierGrains = 64000;
                resinCuFt = "2.0 Cu.Ft";
            }} else {{
                tierGrains = 80000;
                resinCuFt = "2.5 Cu.Ft";
            }}

            const peakGPM = Math.max(8.0, Math.round((baths * 3.5 + 1.5) * 10) / 10);
            const lbsSaltPerRegen = Math.round((tierGrains / 32000) * 6.5);
            const regensPerYear = Math.round(365 / regenDays);
            const bagsPerYear = Math.max(4, Math.ceil((lbsSaltPerRegen * regensPerYear) / 40));

            document.getElementById("resGrainTier").textContent = tierGrains.toLocaleString() + " Gr";
            document.getElementById("resResinCuFt").textContent = resinCuFt + " Resin Bed (" + Math.round(hardness * 17.1) + " PPM)";
            document.getElementById("resPeakGPM").textContent = peakGPM + " GPM";
            document.getElementById("resDailyGrains").textContent = dailyGrains.toLocaleString() + " Gr/Day";
            document.getElementById("resDailyGal").textContent = dailyGallons + " Gal/Day (" + compGPG.toFixed(1) + " Comp GPG)";
            document.getElementById("resSaltBags").textContent = "~" + bagsPerYear + " Bags/Yr";
            document.getElementById("resSaltPerRegen").textContent = lbsSaltPerRegen + " lbs salt per " + regenDays + "-day regen";

            const preFilterText = source === "well"
                ? "50-Micron Spin-Down + Iron/Sediment Filter"
                : "20\" 3-Stage Carbon Chlorine Pre-Filter";
            document.getElementById("resPreFilter").textContent = preFilterText;

            let recTitle = "";
            let recDesc = "";
            let softenerQuery = "";
            let filterQuery = source === "well"
                ? "iSpring Spin Down Sediment Filter and Whole House Iron Filter"
                : "iSpring WGB32B 3 Stage Whole House Water Filter and Waterdrop G3P800 RO";

            if (tierGrains <= 32000) {{
                recTitle = "32,000–40,000 Grain Digital Metered Water Softener (9–11 GPM)";
                recDesc = "Ideal for 1–3 person homes and up to 2.5 bathrooms with moderate hardness.";
                softenerQuery = "32000 40000 Grain Water Softener Fleck 5600SXT Aquasure Harmony Whirlpool";
            }} else if (tierGrains <= 48000) {{
                recTitle = "48,000 Grain Fleck 5600SXT / Aquasure Harmony Softener (12–14 GPM)";
                recDesc = "America's #1 residential capacity for 3–5 people and 3–4 bathrooms.";
                softenerQuery = "48000 Grain Water Softener Fleck 5600SXT Aquasure Harmony Series";
            }} else {{
                recTitle = "64,000–80,000 Grain Heavy-Duty High-Flow Water Softener (15+ GPM)";
                recDesc = "Engineered for large families, 4+ bathrooms, well iron, and 20+ GPG extreme hardness.";
                softenerQuery = "64000 80000 Grain Water Softener Fleck 5600SXT Aquasure";
            }}

            document.getElementById("recSystemTitle").textContent = recTitle;
            document.getElementById("recSystemDesc").textContent = recDesc;
            document.getElementById("recSoftenerBtn").href = makeAmazonLink(softenerQuery);
            document.getElementById("recFilterBtn").href = makeAmazonLink(filterQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateWater);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-700"><span class="text-emerald-600 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-700"><span class="text-rose-600 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-slate-700 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-teal-600">Home & Grain Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-teal-600">System Reviews</a>
            <span>/</span>
            <span class="text-slate-800">{rev['product_name']}</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <span class="text-sm font-black bg-amber-100 text-amber-900 px-3 py-1 rounded-lg">Lab Rating: {rev['rating_score']} / 5.0 ★</span>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-slate-600 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs">
                <div><span class="text-slate-400 block font-medium">Capacity Rating</span><strong class="text-slate-900">{rev['grain_capacity']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Service Flow</span><strong class="text-slate-900">{rev['flow_spec']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Treatment Spec</span><strong class="text-slate-900">{rev['hardness_spec']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Warranty</span><strong class="text-slate-900">{rev['warranty']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-teal-600 hover:bg-teal-700 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-slate-100 hover:bg-slate-200 text-slate-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Grain Size for Your Home
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white border-2 border-emerald-200 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-white border-2 border-rose-200 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-100 pb-3">Water Chemistry & Flow Performance Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-teal-600 block">Final Verdict</span>
                    <p class="text-sm font-bold text-slate-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our residential water treatment test.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-amber-500 hover:bg-amber-600 text-slate-950 font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500 text-center">
        <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-slate-200">
            <td class="p-4 font-bold text-slate-900 bg-slate-50 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-slate-700 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-slate-700 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-teal-600">Home & Grain Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-teal-600">Product Comparisons</a>
            <span>/</span>
            <span class="text-slate-800">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-slate-600 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-white border-2 border-slate-200 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-900 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-teal-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-slate-50">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-slate-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-teal-50 border-2 border-teal-200 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-slate-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-slate-700 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-teal-600 hover:bg-teal-700 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-slate-900 hover:bg-slate-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500 text-center">
        <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "Family of 4 (3 Bathrooms)",
        "people": 4,
        "hardness": 15,
        "iron": 0.5,
        "baths": 3,
        "source": "city",
        "regen_days": 7,
        "desc": "Calculate exact water softener grain capacity (24k–80k grains), peak household GPM flow rate, annual salt usage, and whole-house filtration specs—plus compare top-rated systems."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Programmatic Household & Hardness Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 3. Generate Standalone Product Review Pages
    for rev in PRODUCT_REVIEWS:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} SEO pages (Calculators + Reviews + Comparisons) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
