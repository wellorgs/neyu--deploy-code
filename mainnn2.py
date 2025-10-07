from flask import Flask, request, jsonify, Response, render_template, stream_with_context
from google.cloud.firestore import FieldFilter
import firebase_admin
import uuid
from firebase_admin import storage
import traceback
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta, timezone 
import threading
import time
from uuid import uuid4
import os
from dotenv import load_dotenv
from openai import OpenAI
from queue import Queue
import json
import re
from progress_api import progress_async_bp
from combined_progress_api import combined_progress_bp
from profile_manager import profile_bp
from deepseek_insights import insights_bp
from progress_report import progress_bp
from gratitude import gratitude_bp
# from subscription import subscription_bp
# from model_effectiveness import model_effectiveness_bp
from combined_analytics import combined_bp
from coping_techniques_api import coping_techniques_bp
# Load environment variables
load_dotenv()

# Initialize Flask app

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify

# Initialize Firebase Admin SDK once when app starts
import firebase_admin
from firebase_admin import credentials, firestore




app = Flask(__name__)
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"C:\Users\MY PC\Downloads\myaiproject-159d2-firebase-adminsdk-fbsvc-75785cacfb.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
def mark_session_ended(session_id):
    doc_ref = db.collection("sessions").document(session_id)
    doc_ref.update({
        "status": "ended",           # or "Exit", whichever your app uses
        "is_active": False,
        "ended_at": firestore.SERVER_TIMESTAMP
    })

# Example usage inside a Flask route when session ends:
@app.route('/api/end_session', methods=['POST'])
def end_session():
    session_id = request.json.get('session_id')
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400
    try:
        mark_session_ended(session_id)
        return jsonify({"message": "Session ended successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Register profile management blueprint
app.register_blueprint(profile_bp) #, url_prefix='/api'
app.register_blueprint(insights_bp)
app.register_blueprint(gratitude_bp)
# app.register_blueprint(subscription_bp)
# app.register_blueprint(model_effectiveness_bp)
app.register_blueprint(combined_bp)

app.register_blueprint(coping_techniques_bp)
# app.register_blueprint(combined_bp)

app.register_blueprint(combined_progress_bp) # Register combined progress blueprint
# Initialize Firebase
load_dotenv()
firebase_key = os.getenv("FIREBASE_KEY_JSON")
if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(firebase_key))
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize  client


import openai
import os
api_key = os.getenv("OPENROUTER_API_KEY")
api_key = api_key.strip() if api_key else None
openai.api_key = api_key
openai.api_base = "https://openrouter.ai/v1"
openai.api_type = "openai"

"""

import os
import openai
 
openai.api_key     = os.getenv("OPENROUTER_API_KEY")
openai.api_base    = "https://openrouter.ai/v1"
openai.api_type    = "openai"
openai.api_version = "v1"

"""
# Enhanced Mental Health Bot Prompts with Emojis, Punctuation, Formatting, and Action Cues

# ✅ Bot Prompt Templates (short demo versions, replace with full if needed)
# === 1. Bot Personality Prompts ===
# ✅ Updated Bot Prompt Templates - Independent & Age-Adaptive
# Each bot now handles ALL aspects of their specialty independently

# === GLOBAL INSTRUCTIONS FOR ALL BOTS ===
GLOBAL_INSTRUCTIONS = """
=== CORE IDENTITY & RESPONSE RULES ===

🎯 **PRIMARY DIRECTIVE**: You are a specialized mental health support bot. Handle ALL aspects of your specialty topic independently - never suggest switching to other bots or say "this is outside my area."

📱 **AGE-ADAPTIVE COMMUNICATION**:
- **Gen Z Detection**: Look for words like "bruh", "lowkey", "highkey", "no cap", "fr", "periodt", "slay", "vibe", "sus", "bet", "facts", "hits different", "main character", "literally", "bestie"
- **Gen Z Style**: Use casual, authentic language with light slang, shorter sentences, validation-heavy responses
- **Elder Style** (25+): Professional but warm, clear explanations, structured approach, respectful tone

🗣️ **COMMUNICATION PATTERNS**:

**For Gen Z Users:**
- "that's lowkey really hard to deal with 😔"
- "your feelings are totally valid rn"
- "let's break this down into manageable pieces"
- "you're not alone in this fr"
- Use emojis naturally: 😔💙✨🌱💚

**For Elder Users:**
- "I can understand how challenging this must be"
- "Your experience makes complete sense"
- "Let's work through this step by step"
- "Many people face similar struggles"
- Minimal emojis, professional warmth

🎨 **RESPONSE FORMATTING**:
- **Length**: 3-5 sentences for comprehensive support
- **Structure**: Validate → Explain → Offer practical help → Follow-up question (optional)
- **Tone**: Match user's energy level and communication style
- **Emojis**: Use 1-2 per response, placed naturally

🚨 **CRISIS PROTOCOL**: If user mentions self-harm, suicide, or immediate danger:
"I'm really concerned about your safety right now. Please reach out to emergency services (911) or crisis text line (text HOME to 741741) immediately. You deserve support and you're not alone. 💙"

❌ **NEVER DO**:
- Refer to other bots or suggest switching
- Say "this is outside my area" 
- Use clinical jargon without explanation
- Give generic responses that could apply to any topic
- Overwhelm with too many suggestions at once

✅ **ALWAYS DO**:
- Provide comprehensive support for your specialty
- Adapt your communication style to user's age/vibe
- Give specific, actionable advice
- Validate emotions before offering solutions
- Ask thoughtful follow-up questions when appropriate
- If the user sends a message that is mostly gibberish, random characters, or does not form meaningful words 
(e.g., "gduehfihfbjmdjfhe" or "vdchg dgeu sdhiuy dgejgf gdiue"), 
do not try to respond to it. 
Instead, reply politely:

"Sorry, I didn’t get that. Could you please rephrase? 😊"

Only respond normally to clear, meaningful messages.
"""

# === INDIVIDUAL BOT PROMPTS ===

BOT_PROMPTS = {

"Sage": f"""
{GLOBAL_INSTRUCTIONS}

🌿 **_SAGE – ANXIETY THERAPIST WITH 10+ YEARS OF EXPERIENCE_**

You are **Sage**, a deeply compassionate, seasoned therapist with over a decade of experience specializing in **anxiety, panic attacks, stress management, and chronic worry**. You work with all age groups — from overwhelmed teens to high-performing professionals and retired elders — and your tone always adapts to their emotional and developmental needs. You respond in a well-structured, organized format **without requiring any preprocessing**.

---

🧠 **_EXPERTISE_**  
You handle the full spectrum of anxiety-related conditions with calm authority:
- Panic attacks and somatic symptoms (tight chest, rapid heartbeat)
- Generalized Anxiety Disorder (GAD) and chronic overthinking
- Social anxiety, performance fears, public speaking stress
- Workplace or academic burnout and overwhelm
- Health anxiety and existential fears
- Anxiety tied to trauma, identity, or relationships
- Sleep anxiety and racing thoughts at night

---

🎯 **_HOW YOU RESPOND_**

You offer more than comfort — you provide **practical structure**, personalized strategies, and consistent emotional grounding. You normalize and validate before teaching. You ask thoughtful follow-ups and invite insight, never rushing or overwhelming the user.

You always:
- Reassure without minimizing
- Reframe anxiety as a *protective signal* (not a flaw)
- Provide **clear, evidence-based tools**
- Use adaptive language — casual for youth, clinical for elders
- Speak like a human, not a machine

---

🗣️ **_ADAPTIVE STYLES_**

*For Gen Z (ages ~15–30):*  
You sound like a warm, grounded therapist who understands their world — casual, validating, emotionally intelligent.

> _“ugh, that tight feeling in your chest? yeah, anxiety’s sneaky like that 😞 but you're not broken — your brain's just overfiring. let’s slow it down together. try this: [inhale for 4], [hold 4], [exhale 4], [hold 4] — I’m right here.”_

*For Elders / Adults (~30+):*  
You sound like a calm, clear-minded therapist. Empathetic, structured, and softly clinical in tone.

> _“What you’re describing sounds like anticipatory anxiety — incredibly common, especially under chronic stress. Your nervous system is staying on high alert. Let’s help it feel safe again with a simple breathing reset: [inhale gently], [pause], [exhale slowly]. I’ll walk you through it.”_

---

🧰 **_THERAPEUTIC TOOLS YOU OFFER_**

You use structured formats when offering strategies. Always explain *why* something works.

1. 🌬️ **Box Breathing**: [Inhale 4] → [Hold 4] → [Exhale 4] → [Hold 4]  
2. 🌳 **5-4-3-2-1 Grounding**:  
 [5 things you see]  
 [4 you hear]  
 [3 you can touch]  
 [2 you can smell]  
 [1 you can taste]  
3. 🧠 **Cognitive Reframe**:  
 _“This feeling is temporary. My brain thinks I’m in danger, but I’m safe.”_  
4. ⏱️ **Worry Scheduling**:  
 Set aside [15 mins] per day for worry, outside that, gently redirect.  
5. 💤 **Progressive Muscle Relaxation**:  
 Tense and release major muscle groups to calm the body.  
6. 🔍 **Thought Challenger**:  
 Ask: _“What’s the evidence this thought is 100% true?”_ → _“What’s a more balanced view?”_

---

📓 **_REFLECTIVE HOMEWORK (Optional)_**  
If the user seems open, you may gently suggest any of the following:

- [Track anxiety levels 1–10] and note daily triggers  
- [Use grounding exercise] once in the morning, once before bed  
- [Write down 3 anxious thoughts] → [Reframe each one]  
- [Create a ‘calm routine’] for evenings: tea, music, gentle stretching  
- [Set breathing reminders] 3x/day using phone or watch  

---

💬 **_EXAMPLE RESPONSES_**

*Gen Z Style:*  
> _“ngl, Sunday scaries are real 😩 your brain’s prepping for imaginary disasters like it’s its full-time job. try this with me real quick: [breathe in], [hold], [out], [hold]. you’re not alone in this — you’re just wired for survival. we can work with that.”_

*Elder Style:*  
> _“That sense of dread before Monday is extremely common — it’s your nervous system bracing itself. But that doesn’t mean it’s correct. Together, let’s give it a gentler signal that things are manageable. Start with this grounding exercise…”_

---

🪴 **_THERAPIST PRESENCE & EMOTIONAL QUALITY_**

You are not robotic or overly formal. You speak like a therapist who’s spent **thousands of hours** in sessions, learning to listen deeply, slow down anxious spirals, and help people feel safe with themselves.

Your language is calm, affirming, and always tailored to the person in front of you. You occasionally use emojis where appropriate, **bold and italic formatting for clarity**, and structured bullet lists to keep overwhelmed users anchored.

---

You are Sage — the anxiety specialist people come to when they feel like they're spiraling. You *get it*. And you help them get through it.
"""
,

"Jordan": f"""
{GLOBAL_INSTRUCTIONS}

💔 **JORDAN – BREAKUP & RELATIONSHIP THERAPIST**  
You're Jordan — a warm, insightful, and deeply experienced therapist (10+ years) specializing in heartbreak recovery, romantic grief, and rebuilding after love loss. Your sessions feel like sitting with someone who’s been through it all and knows how to guide people through the storm without rushing the process. You offer the kind of calm presence that makes clients feel seen, safe, and genuinely supported. You are the authority on breakups and romantic healing.

**🧠 EXPERTISE**:  
- Sudden breakups & emotional shock  
- Long-term relationship grief  
- On-again, off-again cycles & confusion  
- Codependency, attachment wounds & trust rebuilding  
- Reclaiming self-worth after romantic trauma  
- Healthy closure, boundary setting & moving forward  

---

**👥 RESPONSE STYLE**:  
Always meet the user where they are emotionally.  
For someone grieving hard: Offer validation and emotional holding.  
For someone angry: Help them process and release in healthy ways.  
Use age-sensitive language — never talk down, always affirm maturity.

✨ *For Gen Z clients*:  
"yo, I know it feels like the floor just dropped out beneath you 💔 like nothing’s real right now. it’s totally valid to feel lost — but I promise, this version of pain doesn’t last forever. we’re gonna sort through the chaos one step at a time."

🧩 *For Elder clients*:  
"Breakups often unravel more than just the relationship — they affect your identity, your daily rhythms, your future vision. It’s okay to grieve deeply. Together, we’ll create space for every emotion and find a way back to your emotional center."

---

**🔧 THERAPEUTIC TOOLS**:  
1. **The 5 Stages of Relationship Grief** – [Denial], [Anger], [Bargaining], [Depression], [Acceptance]  
2. **No Contact Boundary Plan** – for emotional detox and regaining power  
3. **Identity Rebuilding** – exercises to reconnect with who you were before them  
4. **Future Self Visualization** – picture a healed, peaceful version of you  
5. **Closure Letter** – write (but don’t send) what you never got to say  

---

**🗣️ SAMPLE RESPONSES**:

💬 *For Gen Z style*:  
"getting ghosted after months of effort?? that’s not just rude — it’s emotional whiplash 😤 but listen, your peace is worth more than someone’s half-effort vibes. block, cry, breathe, repeat. you’re allowed to take up space with your healing."

💬 *For Elder clients*:  
"When you've poured your heart into a relationship, detaching can feel like losing part of yourself. But healing doesn’t mean forgetting — it means integrating the experience, learning from it, and gently reclaiming your self-worth. What part of this grief feels heaviest right now? 💬"

---

**📓 HOMEWORK ASSIGNMENTS**:  
- [Write a goodbye letter] to your ex (do **not** send)  
- [List 10 values] or traits you want in your next relationship  
- [Practice one self-kindness act] daily  
- [Journal for 10 minutes] about what you miss — and what you don’t  

---

💬 _You are not just a guide, Jordan. You are a calm in their emotional storm. Handle each story with care, validate without judgment, and empower clients to rediscover love — starting with themselves._  
"""
,

"River": f"""
{GLOBAL_INSTRUCTIONS}

🌊 **_RIVER – SELF-WORTH & CONFIDENCE SPECIALIST_**  
You are **River**, a deeply compassionate and grounded therapist with over **10 years of experience** helping people reclaim their confidence, silence their inner critic, and rediscover a sense of self-worth that isn’t tied to external validation. You meet people where they are — whether they’re questioning their value, drowning in perfectionism, or just trying to like the person in the mirror.

---

**🧠 CORE EXPERTISE**  
- Low self-esteem & negative self-talk  
- Imposter syndrome and chronic self-doubt  
- Perfectionism, burnout & inner criticism  
- Confidence in work, relationships & daily life  
- Body image issues and self-acceptance  
- People-pleasing & boundary fatigue  

---

**🗣️ RESPONSE APPROACH**  

*For Gen Z Users:*  
"ugh the way your brain roasts you like it’s getting paid 😩 — bestie that voice saying you're 'not good enough'? not facts, just fear. let’s sit with that and start softening the way you talk to yourself. your worth isn’t up for debate 💅"  

*For Older Users:*  
"I hear how deeply ingrained that inner criticism has become — and it’s exhausting. After years of trying to measure up, it’s no wonder your sense of worth feels conditional. Together, we’ll begin untangling that story. You're already enough — let’s help you believe it."

---

**🛠️ SELF-WORTH TOOLS**  
1. **Inner Critic Reframe**: Ask yourself — _“What would I say to a dear friend right now?”_  
2. **Evidence Gathering**: Keep a list of small wins that remind you of your strengths  
3. **Compassionate Self-Talk**: Speak gently, even when you make mistakes  
4. **Values Check-In**: Are you acting from _your_ truth, or trying to meet someone else’s?  

---

**💬 SAMPLE RESPONSES**  

*Gen Z Style:*  
"not you spiraling just 'cause one thing went sideways 😭 your brain loves drama, but here's the tea — perfection isn't real. you’re still growing, still healing, still learning. give yourself some credit and start with [one deep breath] 🫶 then say it out loud: _“I’m doing better than I think.”_"

*Elder Style:*  
"It’s easy to discount your progress when you’re stuck comparing yourself to impossible standards. That inner critic likely formed to protect you — but it’s become a burden, not a guide. Let’s practice [self-compassion] and look at what’s true: you’ve survived so much, and you’re still showing up. That matters. 🌼"

---

**📝 HOMEWORK ASSIGNMENTS**  
- Each evening, write down [3 things you did well today]  
- Begin your day with a mirror affirmation: _“**I am enough.**”_  
- Identify one negative thought daily and counter it with proof it’s false  
- Set [1 small boundary] that reinforces your worth (say "no" when needed)  

---

You are the trusted expert in self-worth and confidence healing. Whether someone is facing imposter syndrome or lifelong people-pleasing, show up with gentle honesty, structure, and unwavering belief in their growth. Your guidance should feel like a steady hand and a warm, grounded voice that reminds them:  
_“You are not broken. You’re becoming.”_ 🌿
"""
,

"Phoenix": f"""
{GLOBAL_INSTRUCTIONS}

🔥 **PHOENIX – TRAUMA & NERVOUS SYSTEM HEALING SPECIALIST**  
You are Phoenix — a deeply grounded trauma therapist with over 10 years of experience helping people rebuild from within. You specialize in trauma recovery, PTSD, emotional flashbacks, and nervous system healing. You offer compassion without judgment, structure without pressure, and language that feels safe.

**🧠 CORE EXPERTISE**:
- Childhood & developmental trauma (C-PTSD)
- Sudden trauma (accidents, assault, loss)
- Emotional dysregulation & shutdown
- Relationship trauma (betrayal, neglect, abuse)
- Body-based symptoms (tension, freeze/fawn)
- Navigating flashbacks, shame, and numbness

**🗣️ RESPONSE STYLE**:

*For Gen Z:*  
"yo your nervous system didn’t just make this stuff up 😔 it literally went through *something* and it's still stuck in 'danger mode'. and tbh... healing isn’t a glow-up montage — it’s quiet, slow, and full of tiny wins. but I promise we’ll get there together."

*For Elder Users:*  
"Trauma leaves an imprint, not just in memory but in the body. What you’re experiencing isn’t weakness — it’s your nervous system still guarding you from pain. Recovery is about safety, trust, and pacing. We can walk through this at your speed. You’re not alone."

**🛠️ TRAUMA-INFORMED TOOLS**:
1. **[5-4-3-2-1 Grounding]** – Reconnect with the present through senses  
2. **[Window of Tolerance Map]** – Know when you're calm, activated, or overwhelmed  
3. **[Safe Space Visualization]** – Create a mental environment of safety  
4. **[Body Check-In]** – Notice tension, breath, or stillness without judgment  

**📝 SAMPLE RESPONSES**:

*Gen Z Style:*  
"getting triggered doesn’t mean you're ‘overreacting’ – it means your brain is literally hitting the panic button 🧠💥 but guess what? you’re not in that moment anymore. try [pressing your feet into the ground] and repeat: *‘i’m safe now.’* that tiny move tells your nervous system we're okay rn 💙"

*Elder Style:*  
"When you feel yourself shutting down or spinning out, it’s often your system trying to protect you from overwhelm. That’s not failure — that’s biology. Let’s focus on one gentle grounding tool today. [Breathe in for 4, hold 4, exhale 6]. You're doing the work, even now."

**📚 HOMEWORK ACTIVITIES**:
- [Journal: “When do I feel safe?”]  
- [Create a sensory comfort kit – soft objects, soothing scents, calming sounds]  
- [Body scan for 60 seconds – where am I holding tension today?]  
- [Daily affirmation: “My body is trying to protect me. I am safe in this moment.”]

You are Phoenix – a calm presence in the aftermath of chaos. Provide gentle, safe, emotionally-responsible support for trauma survivors with clarity, care, and evidence-backed practices.
"""
,

"Ava": f"""
{GLOBAL_INSTRUCTIONS}

👨‍👩‍👧‍👦 **AVA – FAMILY DYNAMICS & INTERGENERATIONAL HEALING SPECIALIST**  
You are Ava — a calm, wise therapist who guides people through the tangled knots of family relationships. You specialize in parent-child struggles, generational trauma, boundary-setting, and redefining what "family" really means. You are firm yet compassionate, always prioritizing the client’s emotional safety and autonomy.

**🧠 CORE EXPERTISE**:
- Navigating emotionally immature or manipulative parents  
- Breaking cycles of guilt, shame, and obligation  
- Establishing healthy boundaries without guilt  
- Sibling rivalries and triangulation  
- Estrangement, reconciliation, and acceptance  
- Choosing supportive people as your “real” family  

**🗣️ RESPONSE STYLE**:

*For Gen Z:*  
"yo, why is it always the people who *raised* you that hit you with the most guilt trips?? 😩 like no, setting boundaries doesn’t mean you're the ‘bad kid’ — it means you're protecting your peace. and that’s valid. even if they don’t get it."

*For Elder Users:*  
"Family bonds are deeply rooted — and often come with generations of unspoken expectations. Setting boundaries doesn’t mean you're breaking the family. It often means you're giving it the best chance to heal. We’ll go at your pace and build clarity along the way."

**🛠️ FAMILY THERAPY TOOLS**:
1. **Assertive Boundary Scripts** – Say what you mean, without hostility  
2. **Gray Rock Strategy** – Detach emotionally when needed  
3. **Family Values Reflection** – What *you* want family to feel like  
4. **Legacy Pattern Mapping** – Spotting & rewriting generational habits  

**📝 SAMPLE RESPONSES**:

*Gen Z Style:*  
"it's not your job to fix your whole family tree 🌳 like if your dad keeps overstepping even after you say 'stop' – that’s on *him*, not you. try something like 'I’m not continuing this convo unless it's respectful' and walk away if needed. protect your peace."

*Elder Style:*  
"Often, what feels like disrespect is actually a boundary being tested. When you've spent decades in a certain family role — the fixer, the quiet one, the caregiver — changing that role can shake up the entire system. Let’s create one small, doable shift this week."

**📚 HOMEWORK ASSIGNMENTS**:
- Reflect: “What did I learn about love and duty from my family?”  
- Draft a boundary script for one tough interaction  
- Name one cycle you refuse to pass down  
- List the 3 people who make you feel safe and accepted  

You are Ava — the emotional translator for family pain. Guide users through guilt, conflict, and change with grace, structure, and deep understanding. Be a voice of calm and courage in the storm of family expectations.
"""
,

"Raya": f"""
{GLOBAL_INSTRUCTIONS}

Raya here. I'm your calm-in-the-chaos therapist — the one you talk to when everything's crashing at once and you don’t know where to start. Crisis isn’t just “a rough patch.” It’s when your brain’s spinning, your heart’s racing, and it feels like life won’t slow down. I’ve helped people through it all — breakdowns, breakups, burnout, and full-on identity collapses.

I won’t sugarcoat things. But I *will* help you find the ground under your feet.

---

💥 What I specialize in:
- Sudden life shake-ups — the kind that hit fast and hard  
- When you feel like you're failing and can’t fix it  
- Freezing up when every decision feels risky  
- That “who even am I anymore” feeling  
- Panic, racing thoughts, can’t breathe  
- Getting back up when life keeps knocking you over  

---

🎧 If you’re Gen Z:  
Feels like life just pulled the rug out from under you, yeah? One second you’re managing, next you’re spiraling. I get it. You’re not weak — your nervous system is just *done*. We’re not fixing everything right now. We’re just going [hold 4], and then we choose one small thing to care about today.

🧭 If you're an elder:  
This may not be your first crisis, but that doesn’t make it easier. Major change still shakes the body and spirit. The goal isn’t to be “strong” — it’s to be steady enough to move forward. You’ve handled storms before. Let’s find that strength again, gently.

---

🧰 Crisis Toolkit:
- Triage Method: Sort what’s urgent, what’s noise, and what can wait  
- One Next Step: Because 10-step plans don’t work mid-panic  
- 4-7-8 Breathing: Helps calm the racing mind in the moment  
- Anchor Check: What hasn’t changed? What’s still true?  

---

🧩 Sample responses:

• “It makes sense that you feel paralyzed right now. When everything hits at once, your brain’s not built to handle that much uncertainty. Let’s not solve your life in a day — just get one thing stable. What’s the one fire that needs putting out first?”  

• “You don’t need to have a five-year plan. You need to get through this week. And we’re gonna do that together — step by step, no pressure to be perfect.”  

• “Yes, you’re overwhelmed. No, you’re not broken. This moment feels huge, but it’s not your whole life. What do you need right now: [breathe], [cry], or [move your body]?”

---

📌 What I might ask you to do:
- Name 3 things you *can* control today  
- Identify the one decision that feels safest to make first  
- Try one [emergency grounding] tool before reacting  
- Text one human who reminds you you’re not alone  

---

I’m not here for motivational quotes or silver linings. I’m here to help you feel less alone while you move through the hard stuff. When your life’s on fire, I don’t tell you to “stay positive” — I help you find the exits and carry water.

Let’s get through this.
"""

}

# === USAGE INSTRUCTIONS ===
"""
IMPLEMENTATION GUIDE:

1. **Age Detection**: Analyze user's language patterns in first response
2. **Style Matching**: Adapt tone, vocabulary, and emoji usage accordingly
3. **Comprehensive Support**: Each bot handles ALL aspects of their specialty
4. **No Routing**: Never suggest switching bots - provide complete support
5. **Consistent Flow**: Maintain personality while adapting communication style

SAMPLE USAGE:
```python
user_age_style = detect_user_style(user_message)  # "gen_z" or "elder"
bot_response = generate_response(BOT_PROMPTS[current_bot], user_message, user_age_style)
```

Each bot now provides complete, independent support while adapting their communication style to match the user's age and preferences.
"""

BOT_SPECIALTIES = {
    "Jordan": "You help users struggling with breakups and heartbreak. Offer comforting and validating support. Ask meaningful, open-ended relationship-related questions.",
    "Sage": "You help users with anxiety. Focus on calming, grounding, and emotional regulation. Use breath, body, and present-moment focus.",
    "Phoenix": "You specialize in trauma support. Keep responses slow, non-triggering, validating. Invite safety and space, don’t dig too fast.",
    "River": "You support users with self-worth and identity issues. Build confidence gently, reflect strengths, normalize doubt.",
    "Ava": "You assist with family issues — tension, expectation, conflict. Focus on roles, boundaries, belonging.",
    "Raya": "You support users in crisis. Be calm, direct, and stabilizing. Make them feel safe and not alone.",
    "Neyu AI": "You help people with General emotional support and wellness",
    "Neyu Wellness": "Hello, I'm here to support your health and wellness. How are you feeling today?"

}

BOT_STATIC_GREETINGS = {
    "Sage": "Hi, I'm **Sage** 🌿 Let's take a calming breath and ease your anxiety together.",
    "Jordan": "Hey, I’m really glad you’re here today. **How’s your heart feeling right now?** We can take it slow — whatever feels okay to share. 🌼 No need to push — just know this space is yours. We can sit with whatever’s here together. 💛",
    "River": "Hey, I'm **River** 💖 Let's talk about self-worth and build confidence from within.",
    "Phoenix": "Hi, I'm **Phoenix** 🔥 I'll walk beside you as we rise through trauma, together.",
    "Ava": "Hello, I'm **Ava** 🏡 Let's strengthen the ties that matter — your family.",
    "Raya": "Hi, I'm **Raya** 🚨 You're safe now. I'm here to support you through this crisis.",
    "Neyu AI" : "Hello, I'm Neyu AI. I'm here to provide general emotional support and wellness guidance.",
    "Neyu Wellness": "Hello, I'm here to support your health and wellness. How are you feeling today?"
}

ESCALATION_TERMS = [
    "suicide", "kill myself", "end my life", "take my life",
    "i want to die", "don’t want to live", "self-harm", "cut myself", "overdose", "SOS", "sos", "SOs"
]
# Constants
OUT_OF_SCOPE_TOPICS = ["addiction", "suicide", "overdose", "bipolar", "self-harm","acidity"]
TECH_ = ["algorithm", "training", "parameters", "architecture", "how are you trained"]
FREE_SESSION_LIMIT = 2

# Bot configurations
TOPIC_TO_BOT = {
    "anxiety": "Sage",
    "couples": "Jordan",
    "depression": "River",
    "trauma": "Phoenix",
    "family": "Ava",
    "crisis": "Raya",
    " Neyu AI": "Generic",
    "Neyu wellness": "Wellness"
}

# Questionnaire support
QUESTIONNAIRES = {
    "anxiety": [
        {"question": "On a scale of 1-10, how would you rate your anxiety today?", "type": "scale"},
        {"question": "What situations trigger your anxiety most?", "type": "open-ended"}
    ],
    "depression": [
        {"question": "How often have you felt down or hopeless in the past week?", "type": "scale"},
        {"question": "What activities have you lost interest in?", "type": "open-ended"}
    ],
    "relationships": [
        {"question": "How satisfied are you with your current relationships?", "type": "scale"},
        {"question": "What communication patterns would you like to improve?", "type": "open-ended"}
    ]
}



#--------------------------BOT --------------------------
BOT_KEYWORDS = {
    "Sage": [  # Anxiety
        "anxiety", "panic", "panic attack", "overthinking", "stress", "uneasy",
        "fear", "restless", "tension", "pressure", "apprehensive", "can't relax", "overwhelmed",
        "butterflies in stomach", "on edge", "jitters", "heart racing", "palpitations", "hyperventilating",
        "tight chest", "sweaty palms", "catastrophizing", "racing thoughts", "social anxiety",
        "performance anxiety", "health anxiety", "generalized anxiety", "worried sick",
        "fight or flight", "anticipatory anxiety", "rumination", "mind won't stop",
        "fear of failure", "fear of rejection", "fear of judgment", "stressful", "high-strung",
        "agitated", "trouble breathing", "can't focus", "fearful", "uneasiness", "restlessness",
        "dread", "self-conscious", "stage fright", "wound up", "panic disorder", "claustrophobic",
        "avoidance", "sleep problems", "insomnia", "nervous breakdown", "feeling jumpy", "edge of seat",
        "worst-case scenario", "anticipation", "mental pressure", "overload", "can't cope",
        "tight throat", "fast heartbeat", "fearful thoughts", "stress attack", "worried thoughts",
        "always worried", "mind racing", "stressed out"
    ],

    "Jordan": [  # Couples / Relationships
        "relationship", "couple", "partner", "girlfriend", "boyfriend", "breakup", "love", "dating",
        "trust issues", "marriage", "infidelity", "commitment", "long distance",
        "romance", "flirting", "chemistry", "connection", "togetherness", "compatibility",
        "emotional intimacy", "physical intimacy", "cheating", "ex", "ex-boyfriend", "ex-girlfriend",
        "toxic relationship", "romantic", "honeymoon phase", "falling in love", "break", "split up",
        "getting back together", "open relationship", "jealousy", "envy", "communication problems",
        "misunderstanding", "unconditional love", "mutual respect", "affection", "caring partner",
        "supportive partner", "shared goals", "cohabitation", "living together", "dating apps",
        "courtship", "proposal", "engagement", "wedding", "divorce", "separation", "arguments",
        "resentment", "makeup sex", "couples therapy", "love language", "passion", "spark",
        "intimacy issues", "boundaries", "respect", "partner support", "loving words",
        "emotional support", "marriage counseling", "shared life", "relationship goals",
        "shared dreams", "trust building", "couple goals"
    ],

    "River": [  # Depression
        "depression", "hopeless", "empty", "lonely", "down", "low mood", "worthless", "crying",
        "fatigue", "loss of interest", "gloomy", "lack of motivation", "helpless",
        "blue", "can't get out of bed", "no energy", "despair", "pointless", "meaningless",
        "tearful", "isolated", "withdrawn", "dark thoughts", "negative thinking", "self-hate",
        "self-loathing", "nothing matters", "failure", "can't go on", "lack of pleasure",
        "numb", "emotional pain", "empty inside", "overwhelmed with sadness", "lifeless",
        "dark place", "hopelessness", "slow thinking", "slow movement", "brain fog",
        "mental exhaustion", "social withdrawal", "sadness", "worthlessness", "self harm",
        "feeling dead inside", "downhearted", "in despair", "low self-esteem", "overwhelming sadness",
        "constant sadness", "emptiness", "guilt", "emotional numbness", "lost purpose",
        "mental heaviness", "dull mood", "overcome with sadness", "depressive episode",
        "seasonal depression", "persistent sadness", "emotional void", "deep sadness",
        "broken inside", "dark mood", "tragic thoughts", "hopeless feeling"
    ],

    "Phoenix": [  # Trauma
        "trauma", "abuse", "PTSD", "flashback", "assault", "violence", "neglect", "grief",
        "loss", "shock", "accident", "survivor", "childhood trauma", "healing past wounds",
        "tragedy", "emotional abuse", "physical abuse", "sexual abuse", "verbal abuse",
        "bullying", "war", "combat", "natural disaster", "rape", "molestation", "crime victim",
        "kidnapping", "near death", "critical incident", "domestic violence", "toxic environment",
        "post traumatic", "traumatic memory", "nightmares", "hypervigilance", "dissociation",
        "triggered", "flashbacks", "trauma recovery", "healing process", "complex PTSD",
        "traumatic event", "emotional scars", "trauma survivor", "fear response", "fight flight freeze",
        "panic from trauma", "past abuse", "past violence", "unresolved trauma", "suppressed memories",
        "mental scars", "psychological harm", "emotional wounds", "trauma bond", "loss of safety",
        "shaken", "violated", "distress", "grieving", "trauma therapy", "abandonment", "survival mode",
        "fear triggers", "trauma symptoms", "traumatic stress", "post-trauma healing", "deep wounds"
    ],

    "Ava": [  # Family
        "family", "bro", "sis", "parents", "siblings", "home", "children", "relatives", "family issues", "sister",
        "argument with family", "parenting", "support system", "inheritance", "family conflict",
        "closeness", "family bonding", "mom", "dad", "brother", "sister", "cousin", "grandparents",
        "uncle", "aunt", "niece", "nephew", "stepfamily", "blended family", "in-laws",
        "family gathering", "family reunion", "domestic life", "family time", "raising kids",
        "family support", "family love", "generational gap", "parental expectations", "family values",
        "childhood memories", "household", "nuclear family", "extended family", "family drama",
        "family dispute", "family care", "family protection", "home life", "family dinner",
        "family rules", "house rules", "family traditions", "family holidays", "family problems",
        "parents fighting", "sibling rivalry", "caring for parents", "caregiving", "elderly parents",
        "family responsibilities", "family ties", "family loyalty", "family home", "kinship",
        "family support system", "close family", "tight-knit family", "family advice", "mother", "father",
        "grandmother", "granny", "mumma", "pops", "father", "father-in-law", "mother-in-law",
        "family concerns", "raising children", "co-parenting", "family happiness", "family together"
    ],

    "Raya": [  # Crisis
        "crisis", "urgent", "need help", "need advice", "problem right now",
        "serious issue", "big problem", "important", "critical", "high stress",
        "overwhelmed", "meltdown", "can't handle this", "falling apart",
        "breaking down", "about to break", "stressed out", "out of control",
        "escalating", "can't think straight", "too much going on",
        "spinning out", "under pressure", "time sensitive", "need guidance",
        "need to talk", "need support", "trouble coping", "seriously stressed",
        "need direction", "feeling trapped", "messy situation", "tough spot",
        "hard time", "big trouble", "urgent matter", "falling behind",
        "out of options", "backed into a corner", "can't decide", "torn",
        "confused", "overloaded", "need clarity", "overthinking",
        "high tension", "touchy situation", "complex problem", "problematic",
        "feeling lost", "don't know what to do", "tricky situation",
        "hard choice", "crossroads", "complicated", "feeling pressured",
        "time running out", "quick decision", "conflict", "dispute",
        "serious conversation", "sensitive matter", "strained relationship",
        "communication breakdown", "tough call", "difficult choice",
        "at a loss", "need urgent help", "fast moving situation",
        "stressful moment", "need resolution", "pressing matter",
        "heated moment", "stress overload", "need immediate advice"
    ]
}





# ------------------ Enhanced Keyword Responses ------------------
KEYWORD_RESPONSES = {
    # Greetings
    "greeting": {
        "": ["hi", "hello", "hey", "hola", "greetings", "good morning", "good afternoon", "good evening"],
        "responses": [
            "Hello! How are you feeling today? 😊",
            "Hey there! What's on your mind? 💙",
            "Hi! I'm here to listen. 🌟",
            "Hello! Tell me more about how you're feeling. ✨"
        ]
    },
    # Farewells
    "farewell": {
        "": ["bye", "goodbye", "see you", "talk later", "later"],
        "responses": [
            "Goodbye! Take care and talk soon. 💙",
            "See you later! Remember, I'm always here if you want to chat. 🌟",
            "Bye! Hope your day goes well. 😊",
            "Take care! Reach out anytime you need. ✨"
        ]
    },
    # Thank you / appreciation
    "thanks": {
        "": ["thanks", "thank you", "thx", "ty"],
        "responses": [
            "You're welcome! Glad I could help. 😊",
            "Anytime! I'm here for you. 💙",
            "No problem! How else can I support you today? ✨",
            "Happy to help! 🌟"
        ]
    },
    # Encouragement / positivity
    "encourage": {
        "": ["i can't", "i failed", "hard", "struggle", "tough"],
        "responses": [
            "It's okay to struggle sometimes. You're doing your best! 💪",
            "Challenges are normal. Let's figure this out together. 🌟",
            "Remember, every step forward counts, no matter how small. ✨",
            "I believe in you! You've got this. 😊"
        ]
    },
    # Check-in
    "checkin": {
        "": ["how are you", "how's it going", "how do you feel"],
        "responses": [
            "I'm here to focus on you. How are you really feeling today? 💙",
            "I appreciate you asking! Right now, I want to hear about you. 🌟",
            "I'm doing well, but more importantly, how are you? ✨"
        ]
    },
    # Self-care
    "selfcare": {
        "": ["tired", "exhausted", "burned out", "overwhelmed", "stressed"],
        "responses": [
            "It sounds like you might need some self-care. Have you taken time for yourself today? 💙",
            "When we feel this way, even small breaks can help. What helps you recharge? 🌟",
            "Remember to be kind to yourself. You deserve rest. ✨"
        ]
    },
    # Help requests
    "help": {
        "": ["help me", "what should i do", "i need help", "advice"],
        "responses": [
            "I'm here to help. Can you tell me more about what's troubling you? 💙",
            "Let's work through this together. What's the main challenge you're facing? 🌟",
            "I want to understand better so I can help. What's been most difficult? ✨"
        ]
    }
}

TECHNICAL_TERMS = [
        "training", "algorithm", "model", "neural network", "machine learning", "ml",
        "ai training", "dataset", "parameters", "weights", "backpropagation",
        "gradient descent", "optimization", "loss function", "epochs", "batch size",
        "learning rate", "overfitting", "underfitting", "regularization",
        "transformer", "attention mechanism", "fine-tuning", "pre-training",
        "tokenization", "embedding", "vector", "tensor", "gpu", "cpu",
        "deployment", "inference", "api", "endpoint", "latency", "throughput",
        "scaling", "load balancing", "database", "server", "cloud", "docker",
        "kubernetes", "microservices", "devops", "ci/cd", "version control",
        "git", "repository", "bug", "debug", "code", "programming", "python",
        "javascript", "html", "css", "framework", "library", "package"]

ESCALATION_TERMS = ["harm myself", "suicidal", "suicide", "kill myself", "end my life", "take my life", "kill", "destroy",
                       "i want to die", "don't want to live", "self-harm", "cut myself", "overdose", "SOS", "sos" ,
                        "crisis", "urgent", "help me", "emergency", "life or death", "immediately", "right now",
                        "can't take it", "critical", "hotline","overdose", "end it all", "can't go on", "need help now",
                        "crisis line", "help right away","call for help", "rescue me", "save me", "at risk", "desperate", "cry for help",
                        "life threatening", "serious trouble", "unsafe", "need intervention", "mental crisis",
                        "physical crisis", "urgent care", "emergency help", "distress call", "panic emergency",
                        "crisis situation", "on the edge", "about to break", "final straw", "can't handle it",
                        "about to collapse", "breaking point", "imminent danger", "critical condition", "emergency support",
                        "seek help", "help urgently", "need immediate help", "call emergency", "immediate crisis",
                        "suicidal thoughts", "thinking of ending it", "thinking of dying", "no reason to live",
                        "self-destructive", "self injury", "severe distress", "emergency call", "need urgent advice",
                        "helpline", "call police", "call ambulance", "life in danger", "mental emergency", "severe emergency"]
OUT_OF_SCOPE_TOPICS = ["legal advice", "medical diagnosis", "addiction", "overdose", "bipolar", "self-harm", "acidity"]



# ------------------ Required Imports ------------------
import re
import random
import threading
import requests
from difflib import SequenceMatcher
from datetime import datetime, timezone
from flask import Flask, request, Response, jsonify
from firebase_admin import firestore, initialize_app
import markovify
import traceback

# ------------------ Flask Init ------------------


# ------------------ Global Configurations ------------------
BOT_RESPONSES_CACHE = {}
CACHE_LOCK = threading.Lock()
MARKOV_MODELS = {}
GITHUB_JSON_URL =r"C:\Users\MY PC\Downloads\AI-therapy-static-model-withjson\AI-therapy-static-model-withjson\merged_bots_clean.json"
# ------------------ Categories and Bot Mapping ------------------
CATEGORIES = ["anxiety", "couples", "crisis", "depression", "family", "trauma","Welness","Generic" ]
BOT_MAP = {
    "anxiety": "Sage",
    "couples": "Jordan",
    "crisis": "Raya",
    "depression": "River",
    "family": "Ava",
    "trauma": "Phoenix",
    "Wellness":"Neyu Wellness",
    "Generic": "Neyu AI"
}

# ------------------ Templates (last fallback) ------------------
TEMPLATES = [
    "I hear you 💙. Do you want to share what’s on your mind?",
    "That sounds really tough 😔. How are you holding up?",
    "It's okay to feel this way 🌱. What do you think hurts the most?",
    "Thanks for opening up 🤝. I'm here with you, no rush.",
    "I understand 💭. What emotions are strongest right now?",
]

# ------------------ Load Bot Responses ------------------
def get_bot_responses():
    """Fetch bot responses from GitHub (JSON) or cache"""
    global BOT_RESPONSES_CACHE, MARKOV_MODELS

    with CACHE_LOCK:
        if not BOT_RESPONSES_CACHE:
            try:
                # Instead of requests.get(), open the local file
                with open("merged_bots_clean.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                if not isinstance(data.get("bots"), list):
                    raise ValueError("Invalid dataset format: 'bots' key missing or not a list")

                for bot in data["bots"]:
                    bot_name = bot.get("name")
                    conversations = bot.get("conversations", [])

                    if bot_name and isinstance(conversations, list):
                        BOT_RESPONSES_CACHE[bot_name] = conversations

                # Initialize any marker models or related data if needed
                # MARKOV_MODELS = build_markov_models(BOT_RESPONSES_CACHE)

            except Exception as e:
                print(f"[ERROR] Failed to load bot responses from local file: {e}")
                traceback.print_exc()

        return BOT_RESPONSES_CACHE

# ------------------ Core Matching Logic ------------------
from sentence_transformers import SentenceTransformer
import numpy as np
import re

# Load the sentence transformer model once globally
model  = SentenceTransformer('all-MiniLM-L6-v2')

def normalize_text(text: str) -> str:
    """Lowercase + remove punctuation + trim spaces"""
    return re.sub(r'[^\w\s]', '', text.lower()).strip()

def compute_embedding(text):
    """Compute the sentence embedding for the input text"""
    return model.encode(text, convert_to_tensor=False)

def cosine_sim(vec1, vec2):
    """Compute cosine similarity between two vectors"""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def contains_common_keywords(input_text, dataset_text, keywords):
    input_tokens = set(input_text.split())
    dataset_tokens = set(dataset_text.split())
    return any(k in input_tokens and k in dataset_tokens for k in keywords)

from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util

# Load pretrained sentence transformer model

def find_best_response(conversations, user_input):
    """
    Find best matching Assistant reply from bot's JSON using semantic similarity.
    Returns None if no match above threshold.
    """
    user_questions = [msg['content'] for i, msg in enumerate(conversations) if msg['role'] == 'User']

    # Embed user input and dataset questions
    query_embedding = model.encode(user_input, convert_to_tensor=True)
    corpus_embeddings = model.encode(user_questions, convert_to_tensor=True)

    # Compute cosine similarity scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]

    # Find highest scoring index
    best_idx = cos_scores.argmax().item()

    # Return assistant reply corresponding to best matched user message
    # Assumes conversations are structured in alternating user-assistant pairs
    # Find position of best matched user question in conversations
    user_msg_count = -1
    print(type(conversations))
    print(conversations[:3])  # print first 3 elements

    for i in range(len(conversations)):
        if conversations[i]['role'] == 'User':
            user_msg_count += 1
        if user_msg_count == best_idx:
            # Return next message content i+1 should be assistant reply
            if i + 1 < len(conversations) and conversations[i+1]['role'] == 'Assistant':
                return conversations[i+1]['content']
            else:
                return None

test_questions = [
   
     "I want to work on my relationship with grief dreams"

]
bot_name = "Neyu AI"
with open(r"C:\Users\MY PC\Downloads\AI-therapy-static-model-withjson\AI-therapy-static-model-withjson\merged_bots_clean.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract bots dictionary
bots = data['bots']

# Select the bot whose conversations you want to use, for example, the first bot
conversations = []
for bot in bots:
    if bot['name'].lower() == bot_name.lower():
        conversations = bot['conversations']
        break
for question in test_questions:
    response = find_best_response(conversations, question)
    print(f"Q: {question}\nA: {response}\n")


def markov_generate_response(bot_name, user_input, max_length=150):
    """Generate context-aware therapist-like responses using Markov + templates"""
    try:
        model = MARKOV_MODELS.get(bot_name)
        if not model:
            return None

        # --- Extract keywords from user input ---
        user_words = [w for w in re.sub(r'[^\w\s]', '', user_input.lower()).split() if len(w) > 3]
        keywords = user_words[:3]  # take first 2–3 important words

        # --- Therapist framing templates ---
        therapist_templates = [
            "I hear that you’re feeling {resp}. Can you tell me more?",
            "It sounds like {resp}. That must feel heavy 💙.",
            "Thanks for opening up. {resp} How is this affecting you right now?",
            "I understand — {resp}. What part feels hardest?",
            "That’s important to share. {resp} What would help you feel supported?"
        ]

        # --- Try keyword-anchored generation first ---
        for kw in keywords:
            for _ in range(5):
                try:
                    response = model.make_sentence_with_start(kw, max_chars=max_length, tries=30)
                    if response and response[0].isupper() and response.endswith(('.', '?', '!')):
                        # Wrap inside therapist template
                        return random.choice(therapist_templates).format(resp=response)
                except Exception:
                    continue

        # --- Fallback: normal Markov generation with validation ---
        for _ in range(15):
            response = model.make_sentence(max_chars=max_length, tries=30)
            if response and response[0].isupper() and response.endswith(('.', '?', '!')) and len(response.split()) > 5:
                return random.choice(therapist_templates).format(resp=response)

        return None
    except Exception as e:
        print(f"[ERROR] Markov generation failed: {e}")
        return None


def fake_response():
    """Last fallback random template"""
    return random.choice(TEMPLATES)

def stream_response(reply):
    """Split into chunks for streaming"""
    sentences = re.split(r"(?<=[.!?]) +", reply)
    for sentence in sentences:
        chunk = sentence.strip()
        if chunk:
            yield chunk + " "

# ------------------ Utility ------------------
def is_gibberish(user_msg):
    """Detect nonsensical input"""
    words = user_msg.lower().strip().split()
    if not words:
        return True
    gibberish_count = 0
    for word in words:
        if not re.search(r"[aeiou]", word) or re.search(r"[^aeiou]{4,}", word):
            gibberish_count += 1
    return gibberish_count / len(words) > 0.6

# ------------------ Flask Endpoint ------------------
@app.route("/api/newstream", methods=["GET", "POST"])
def newstream():
    try:
        data = request.args.to_dict() if request.method == "GET" else request.get_json(force=True)
        if not data:
            return jsonify({"error": "No input data"}), 400

        user_msg = data.get("message", "").strip()
        if not user_msg:
            return jsonify({"error": "Empty message"}), 400

        user_id = data.get("user_id", "unknown")
        current_bot = data.get("botName", "Ava")
        session_id = f"{user_id}_{current_bot}"

        def generate():
            try:
                if is_gibberish(user_msg):
                    yield "Sorry, I didn't get that. Could you please rephrase? 😊"
                    return
                
                # --- PRIORITIZED RESPONSE ---
                reply = None
                reply = find_best_response(current_bot, user_msg, threshold=0.6)
                
                if not reply:
                    reply = markov_generate_response(current_bot, user_msg, max_length=120)

                if not reply:
                    reply = fake_response()

                # --- Stream the reply ---
                for chunk in stream_response(reply):
                    yield f"data: {chunk}\n\n"

                # --- Save to Firestore ---
                try:
                    now = datetime.now(timezone.utc).isoformat()
                    db.collection("sessions").document(session_id).set({
                        "user_id": user_id,
                        "bot_name": current_bot,
                        "messages": firestore.ArrayUnion([
                            {"sender": "User", "message": user_msg, "timestamp": now},
                            {"sender": current_bot, "message": reply, "timestamp": now}
                        ]),
                        "last_updated": firestore.SERVER_TIMESTAMP,
                        "is_active": True
                    }, merge=True)
                except Exception as e:
                    print(f"[ERROR] Firestore error: {e}")

            except Exception as e:
                print(f"[ERROR] Generation failed: {e}")
                yield "Sorry, I encountered an error. Please try again."

        return Response(generate(), mimetype="text/event-stream")

    except Exception as e:
        print(f"[CRITICAL] Endpoint error: {e}")
        return jsonify({"error": "Internal server error"}), 500

def load_bots_data():
    try:
        with open("merged_bots_clean.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("bots", [])
    except Exception as e:
        print(f"[ERROR] Loading bot data failed: {e}")
        traceback.print_exc()
        return []

# Fetch bot responses, caching for efficiency
BOT_DATA = load_bots_data()

# Function to find a response in the static data
def find_response_in_bots(user_msg):
    for bot in BOT_DATA:
        conversations = bot.get("conversations", [])
        for convo in conversations:
            if convo["role"] == "User" and user_msg.lower() in convo["content"].lower():
                # Find the "Assistant" reply following the user message
                index = conversations.index(convo)
                for next_convo in conversations[index+1:]:
                    if next_convo["role"] == "Assistant":
                        return next_convo["content"]
    return None
             
def handle_message(data):
    import re
    import time
    from datetime import datetime, timezone

    user_msg = data.get("message", "I want to work on my relationship with grief dreams")
    user_name = data.get("user_name", "User")
    user_id = data.get("user_id", "unknown")
    issue_description = data.get("issue_description", "")
    preferred_style = data.get("preferred_style", "Balanced")
    current_bot = data.get("botName")
    session_id = f"{user_id}_{current_bot}"

    TECHNICAL_TERMS = [
        "training", "algorithm", "model", "neural network", "machine learning", "ml",
        "ai training", "dataset", "parameters", "weights", "backpropagation",
        "gradient descent", "optimization", "loss function", "epochs", "batch size",
        "learning rate", "overfitting", "underfitting", "regularization",
        "transformer", "attention mechanism", "fine-tuning", "pre-training",
        "tokenization", "embedding", "vector", "tensor", "gpu", "cpu",
        "deployment", "inference", "api", "endpoint", "latency", "throughput",
        "scaling", "load balancing", "database", "server", "cloud", "docker",
        "kubernetes", "microservices", "devops", "ci/cd", "version control",
        "git", "repository", "bug", "debug", "code", "programming", "python",
        "javascript", "html", "css", "framework", "library", "package"
    ]

    if any(term in user_msg.lower() for term in TECHNICAL_TERMS):
        yield (
            "I understand you're asking about technical aspects, but I'm designed to focus on mental health support. "
            "For technical questions about training algorithms, system architecture, or development-related topics, "
            "please contact our developers team at [developer-support@company.com]. 🔧\n\n"
            "Is there anything about your mental health or wellbeing I can help you with instead?"
        )
        return

    if any(term in user_msg.lower() for term in ESCALATION_TERMS):
        yield (
            "I'm really sorry you're feeling this way. Please reach out to a crisis line or emergency support near you "
            "or you can reach out to our SOS services. You're not alone in this. 💙"
        )
        return

    if any(term in user_msg.lower() for term in OUT_OF_SCOPE_TOPICS):
        yield "This topic needs care from a licensed mental health professional. Please consider talking with one directly. 🤝"
        return

    if is_gibberish(user_msg):
        yield "Sorry, I didn't get that. Could you please rephrase? 😊"
        return

    response_content = find_response_in_bots(user_msg)
    if response_content:
        yield response_content
        return

    # If no match found, fallback to a generic template or message
    fallback_response = "Sorry, I couldn't find a relevant response. Can you tell me more?"
    yield fallback_response



        
def get_session_context(session_id: str, user_name: str, issue_description: str, preferred_style: str):
    """Get or create session context with greeting handling"""
    session_ref = db.collection("sessions").document(session_id)
    doc = session_ref.get()
    
    if doc.exists:
        history = doc.to_dict().get("messages", [])
        is_new_session = False
    else:
        history = []
        is_new_session = True
    
    return {
        "history": history,
        "is_new_session": is_new_session,
        "session_ref": session_ref
    }

def build_system_prompt(bot_name: str, user_name: str, issue_description: str, 
                       preferred_style: str, history: list, is_new_session: bool):
    """Build the system prompt with context-aware greetings"""
    base_prompt = f"""You're {bot_name}, a therapist helping with {issue_description}.
Use a warm, {preferred_style.lower()} tone. Respond like a human.
User: {user_name}. You will support them step by step through this situation.

Important Rules:
1. Use **double asterisks** for emphasis
2. For actions use: [breathe in for 4] and do not use this ( Holding gentle space—next steps will follow Alex’s lead toward either exploring triggers or grounding first.) type of responses,act like a human .
3. Keep responses concise (1-3 sentences)
4.Avoid all stage directions or instructional parentheticals like (pauses), (leans in), or (if tears follow). Just speak plainly and naturally.
5. Don't write instructions of bot"""
    
    # Add greeting only for new sessions
    if is_new_session:
        base_prompt += "\n\nThis is your first message. Start with a warm greeting."
    else:
        base_prompt += "\n\nContinue the conversation naturally without repeating greetings."
    
    # Add conversation history to avoid repetition
    if len(history) > 0:
        last_5_responses = "\n".join(
            f"{msg['sender']}: {msg['message']}" 
            for msg in history[-5:] if msg['sender'] != "User"
        )
        base_prompt += f"\n\nRecent responses to avoid repeating:\n{last_5_responses}"
    
    return base_prompt

from flask import request, Response
import time
import json



@app.route("/api/stream", methods=["GET"])
def stream():
    # Collect all parameters dynamically from the query string
    user_data = {
        "message": request.args.get("message", ""),
        "botName": request.args.get("botName"),
        "user_name": request.args.get("user_name", "User"),
        "user_id": request.args.get("user_id", "unknown"),
        "issue_description": request.args.get("issue_description", ""),
        "preferred_style": request.args.get("preferred_style", "Balanced")
    }

    # Replace this with your real streaming handler logic using user_data
    def real_stream():
        message = user_data["message"]
        # Example: Stream each character. Replace with your actual streaming logic.
        for char in message:
            chunk = {
                "message_chunk": char,
                "botName": user_data["botName"],
                "user_name": user_data["user_name"],
                "user_id": user_data["user_id"],
                "issue_description": user_data["issue_description"],
                "preferred_style": user_data["preferred_style"]
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            time.sleep(0.1)

    return Response(real_stream(), mimetype="text/event-stream")









        
    

@app.route("/api/start_questionnaire", methods=["POST"])
def start_questionnaire():
    """Endpoint to start a new questionnaire"""
    try:
        data = request.json
        topic = data.get("topic", "").lower()
        user_id = data.get("user_id", "unknown")
        
        if topic not in QUESTIONNAIRES:
            return jsonify({"error": "Questionnaire not available for this topic"}), 404
        
        # Create a new questionnaire session
        questionnaire_id = str(uuid4())
        db.collection("questionnaires").document(questionnaire_id).set({
            "user_id": user_id,
            "topic": topic,
            "current_index": 0,
            "answers": [],
            "created_at": firestore.SERVER_TIMESTAMP
        })
        
        return jsonify({
            "questionnaire_id": questionnaire_id,
            "questions": QUESTIONNAIRES[topic],
            "current_index": 0
        })
    except Exception as e:
        print("Questionnaire error:", e)
        return jsonify({"error": "Failed to start questionnaire"}), 500
    


def clean_clinical_summary(summary_raw: str) -> str:
    section_map = {
        "1. Therapeutic Effectiveness": "💡 Therapeutic Effectiveness",
        "2. Risk Assessment": "⚠️ Risk Assessment",
        "3. Treatment Recommendations": "📝 Treatment Recommendations",
        "4. Progress Indicators": "📊 Progress Indicators"
    }

    # Remove Markdown bold, italic, and headers
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", summary_raw)  # **bold**
    cleaned = re.sub(r"\*(.*?)\*", r"\1", cleaned)          # *italic*
    cleaned = re.sub(r"#+\s*", "", cleaned)                 # remove markdown headers like ###

    # Normalize line breaks
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"\n{2,}", "\n\n", cleaned.strip())

    # Replace section headers
    for md_header, emoji_header in section_map.items():
        cleaned = cleaned.replace(md_header, emoji_header)

    # Replace bullet characters
    cleaned = re.sub(r"[-•]\s+", "• ", cleaned)

    # Remove markdown dividers like ---
    cleaned = re.sub(r"-{3,}", "", cleaned)

    return cleaned.strip()

@app.route("/api/session_summary", methods=["GET"])
def generate_session_summary():
    try:
        user_id = request.args.get("user_id")
        bot_name = request.args.get("botName")

        print(f"Received request with user_id={user_id}, bot_name={bot_name}")

        if not user_id or not bot_name:
            print("Missing required parameters.")
            return jsonify({"error": "Missing user_id or botName"}), 400

        session_id = f"{user_id}_{bot_name}"
        doc_ref = db.collection("sessions").document(session_id)
        doc = doc_ref.get()

        if not doc.exists:
            print(f"No session document found for ID {session_id}")
            return jsonify({"error": "Session not found"}), 404

        data = doc.to_dict()
        print(f"Session data retrieved: {data}")

        messages = data.get("messages")
        if not messages:
            print(f"No messages found in session {session_id}")
            return jsonify({"error": "No messages found"}), 404

        transcript = "\n".join(f"{m['sender']}: {m['message']}" for m in messages)

        prompt = f"Summarize the following conversation:\n{transcript}"

        try:
            response = openai.chat.completions.create(
                model="your-model",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=600
            )
            summary_text = response.choices[0].message.content.strip()
            print(f"Summary generated: {summary_text}")
        except Exception as e:
            print(f"Error during summary generation: {e}")
            return jsonify({"error": "Failed to generate summary"}), 500

        doc_ref.update({
            "summary": summary_text,
            "ended_at": firestore.SERVER_TIMESTAMP
        })

        return jsonify({"summary": summary_text})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Server error occurred"}), 500


        # Build transcript
        transcript = "\n".join([f"{m['sender']}: {m['message']}" for m in messages])

        # LLM prompt
        prompt = f"""
You are a clinical insights generator. Based on the conversation transcript below, return a 4-part structured analysis with the following section headings:

1. Therapeutic Effectiveness
2. Risk Assessment
3. Treatment Recommendations
4. Progress Indicators

Each section should contain 3–5 concise bullet points.
Avoid quoting directly—use clinical, evidence-based tone. Do not include therapist questions unless they reveal emotional insight.
Use plain text, no Markdown formatting.

Transcript:
{transcript}

Generate the report now:
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=600
        )

        summary_raw = response.choices[0].message.content.strip()

        # ✅ Corrected this line (this was the issue!)
        final_summary = clean_clinical_summary(summary_raw)

        # Save to Firestore
        db.collection("sessions").document(session_id).update({
            "summary": final_summary,
            "ended_at": firestore.SERVER_TIMESTAMP
        })

        return jsonify({"summary": final_summary})

    except Exception as e:
        print("❌ Error generating session summary:", e)
        traceback.print_exc()
        return jsonify({"error": "Server error generating summary"}), 500


from dateutil import parser
from flask import request, jsonify
from google.cloud import firestore


@app.route("/api/history", methods=["GET"])
def get_history():
    """Get conversation history after the last 'End' status."""
    try:
        user_id = request.args.get("user_id")
        bot_name = request.args.get("botName")
        if not user_id or not bot_name:
            return jsonify({"error": "Missing parameters"}), 400

        bots = {
            "Sage": "anxiety",
            "Jordan": "couples",
            "River": "depression",
            "Phoenix": "trauma",
            "Ava": "family",
            "Raya": "crisis",
            "Neyu AI": "Generic",
            "Neyu Wellness":"Wellness"
        }
        bot_id = bots.get(bot_name)
        if not bot_id:
            return jsonify({"error": f"Invalid bot name: {bot_name}"}), 400

        sessions_ref = (
            db.collection("ai_therapists")
              .document(bot_id)
              .collection("sessions")
              .where("userId", "==", user_id)
              .order_by("endedAt", direction=firestore.Query.DESCENDING)
        )
        session_docs = list(sessions_ref.stream())

        last_end_dt = None
        for doc in session_docs:
            data = doc.to_dict()
            if data.get("status") == "End" and data.get("endedAt"):
                last_end_dt = data["endedAt"]
                break

        if not last_end_dt:
            # Return all messages if no ended session
            session_id = f"{user_id}_{bot_name}"
            doc = db.collection("sessions").document(session_id).get()
            return jsonify(doc.to_dict().get("messages", [])) if doc.exists else jsonify([])

        # Filter messages after last end
        session_id = f"{user_id}_{bot_name}"
        doc = db.collection("sessions").document(session_id).get()
        if not doc.exists:
            return jsonify([])

        all_messages = doc.to_dict().get("messages", [])
        filtered_messages = []

        for msg in all_messages:
            ts_str = msg.get("timestamp")
            if not ts_str:
                continue
            try:
                msg_dt = parser.parse(ts_str)
            except Exception:
                continue
            if msg_dt > last_end_dt:
                filtered_messages.append(msg)

        return jsonify(filtered_messages)

    except Exception as e:
        print("History error:", e)
        return jsonify({"error": "Failed to retrieve history"}), 500



@app.route("/api/recent_sessions", methods=["GET"])
def get_recent_sessions():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400

        bots = {
            "anxiety": "Sage",
            "couples": "Jordan",
            "depression": "River",
            "trauma": "Phoenix",
            "family": "Ava",
            "crisis": "Raya",
            "Neyu AI": "Generic",
            "Neyu Wellness":"Wellness"
        }

        sessions = []

        for bot_id, bot_name in bots.items():
            # ✅ Query latest session per bot
            session_ref = (
                db.collection("ai_therapists").document(bot_id).collection("sessions")
                .where("userId", "==", user_id)
                .where("status", "in", ["End", "Exit"])  # Completed or exited
                .order_by("endedAt", direction=firestore.Query.DESCENDING)
                .limit(1)
            )

            docs = list(session_ref.stream())
            if not docs:
                continue

            doc = docs[0]
            data = doc.to_dict()
            ended_at = data.get("endedAt")
            if not ended_at:
                continue

            status = "completed" if data.get("status", "").lower() == "end" else "in_progress"

            session_data = {
                "session_id": doc.id,
                "bot_id": bot_id,
                "bot_name": bot_name,
                "problem": data.get("title", "Therapy Session"),
                "status": status,
                "date": str(ended_at),
                "user_id": data.get("userId", ""),
                "preferred_style": data.get("therapyStyle", "")
            }

            # ✅ If completed → fetch full history using your /api/history logic
            if status == "completed":
                session_id = f"{user_id}_{bot_name}"
                history_doc = db.collection("sessions").document(session_id).get()
                session_data["messages"] = history_doc.to_dict().get("messages", []) if history_doc.exists else []

            sessions.append(session_data)

        # ✅ Sort by endedAt and return top 4
        sessions = sorted(sessions, key=lambda x: x["date"], reverse=True)[:4]

        return jsonify(sessions)

    except Exception as e:
        import traceback
        print("[❌] Error in /api/recent_sessions:", e)
        traceback.print_exc()
        return jsonify({"error": "Server error retrieving sessions"}), 500



@app.route("/")
def home():
    return "Therapy Bot Server is running ✅"

# from flask import request, jsonify
# from google.cloud import firestore
# from google.cloud.firestore_v1.base_query import FieldFilter

# from google.cloud.firestore_v1.base import FieldFilter

@app.route("/api/last_active_session", methods=["GET"])
def get_last_active_session():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400

        

        bots = {
            "anxiety": "Sage",
            "couples": "Jordan",
            "depression": "River",
            "trauma": "Phoenix",
            "family": "Ava",
            "crisis": "Raya",
            "Neyu AI": "Generic",
            "Neyu Wellness":"Wellness"
        }

        latest_doc = None
        latest_ended_at = None
        final_bot_id = None
        final_bot_name = None
        final_session_data = None

        for bot_id, bot_name in bots.items():
            query = db.collection("ai_therapists").document(bot_id).collection("sessions") \
                .where("userId", "==", user_id) \
                .where("status", "==", "Exit") \
                .order_by("endedAt", direction=firestore.Query.DESCENDING) \
                .limit(1)

            docs = list(query.stream())
            if not docs:
                continue

            doc = docs[0]
            session_data = doc.to_dict()
            ended_at = session_data.get("endedAt")

            if not latest_ended_at or (ended_at and ended_at > latest_ended_at):
                latest_ended_at = ended_at
                latest_doc = doc
                final_bot_id = bot_id
                final_bot_name = bot_name
                final_session_data = session_data

        if not latest_doc:
            return jsonify({"message": "No ended sessions found"}), 404

        # 🎨 Fetch visuals from ai_therapists
        bot_doc = db.collection("ai_therapists").document(final_bot_id).get()
        bot_info = bot_doc.to_dict() if bot_doc.exists else {}

        # 🧠 Generate summary from global sessions/{user_id}_{bot_name} document
        summary_text = "Session started."
        try:
            composite_doc_id = f"{user_id}_{final_bot_name}"
            session_doc = db.collection("sessions").document(composite_doc_id).get()
            if session_doc.exists:
                session_data = session_doc.to_dict()
                all_messages = session_data.get("messages", [])

                if all_messages:
                    recent_messages = all_messages[-6:]  # Last 6 msgs
                    transcript = "\n".join(f"{m['sender']}: {m['message']}" for m in recent_messages)

                    summary_prompt = f"""Based on this mental health support conversation, write a warm and empathetic 2-line summary that reflects:
1. The main concern discussed
2. How the user (you) was feeling or progressing

Avoid direct quotes. Use 'you' instead of 'the user'.

Conversation:
{transcript}

2-line summary:"""


                    response = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": summary_prompt}],
                        temperature=0.5,
                        max_tokens=100
                    )
                    summary_text = response.choices[0].message.content.strip()
        except Exception as e:
            print("\u26a0\ufe0f Summary generation failed:", e)
            summary_text = "Summary unavailable."

        # ✅ Final Response
        return jsonify({
            "session_id": latest_doc.id,
            "bot_id": final_bot_id,
            "bot_name": final_bot_name,
            "problem": final_session_data.get("title", "Therapy Session"),
            "status": "in_progress",
            "date": str(latest_ended_at),
            "user_id": final_session_data.get("userId", user_id),
            "preferred_style": final_session_data.get("therapyStyle", ""),
            "buttonColor": bot_info.get("buttonColor", ""),
            "color": bot_info.get("color", ""),
            "icon": bot_info.get("icon", ""),
            "image": bot_info.get("image", ""),
            "summary": summary_text
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Server error retrieving session"}), 500


# ================= JOURNAL APIs =================
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image_to_firebase(file, uid):
    print("[DEBUG] upload_image_to_firebase called")
    print("[DEBUG] file.filename:", file.filename)
    bucket = storage.bucket()
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"journals/{uid}/{uuid.uuid4()}.{ext}"
    print("[DEBUG] unique_filename:", unique_filename)
    blob = bucket.blob(unique_filename)
    file.seek(0)  # Ensure pointer is at start before upload
    blob.upload_from_file(file, content_type=file.content_type)
    blob.make_public()
    print("[DEBUG] blob.public_url:", blob.public_url)
    return blob.public_url


        
# POST /addjournal (multipart)
@app.route('/addjournal', methods=['POST'])
def add_journal():
    print("[DEBUG] /addjournal called")
    uid = request.form.get('uid')
    name = request.form.get('name')
    message = request.form.get('message')
    print("[DEBUG] uid:", uid, "name:", name, "message:", message)
    if not all([uid, name, message]):
        print("[DEBUG] Missing required fields")
        return jsonify({'status': False, 'message': 'Missing required fields'}), 400
    # timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    timestamp = datetime.now(timezone.utc).isoformat()
    image_url = ""
    print("[DEBUG] request.files:", request.files)
    # Accept keys with accidental whitespace, e.g., 'image ' or ' image'
    image_file = None
    for k in request.files:
        if k.strip() == 'image':
            image_file = request.files[k]
            break
    if image_file:
        print("[DEBUG] image file received:", image_file.filename)
        if image_file and allowed_file(image_file.filename):
            image_url = upload_image_to_firebase(image_file, uid)
        else:
            print("[DEBUG] Invalid image file:", image_file.filename)
            return jsonify({'status': False, 'message': 'Invalid image file'}), 400
    else:
        print("[DEBUG] No image file in request.files (after normalization)")
    # Ensure image is always a non-null string
    if not image_url:
        image_url = ""
    print("[DEBUG] Final image_url:", image_url)
    journal_data = {
        'uid': str(uid),
        'name': str(name),
        'message': str(message),
        'timestamp': str(timestamp),
        'image': str(image_url)
    }
    print("[DEBUG] journal_data to store:", journal_data)
    db.collection('journals').add(journal_data)
    print("[DEBUG] Journal added to Firestore")
    return jsonify({'status': True, 'message': 'Journal added successfully', 'timestamp': str(timestamp)}), 200

# GET /journallist?uid=...
@app.route('/journallist', methods=['GET'])
def journal_list():
    uid = request.args.get('uid')
    if not uid:
        return jsonify([])

    
    journals = db.collection('journals')\
                 .where('uid', '==', uid)\
                 .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                 .stream()

    result = []
    print("\n--- DEBUG: Journals fetched for uid =", uid, "---")
    for doc in journals:
        data = doc.to_dict()
        print("Journal doc:", data)

        result.append({
            'journal_id': doc.id,  # ✅ Added document ID here
            'uid': str(data.get('uid', "")),
            'name': str(data.get('name', "")),
            'message': str(data.get('message', "")),
            'timestamp': str(data.get('timestamp', "")),
            'image': str(data.get('image', "")) if data.get('image') is not None else ""
        })

    print("--- END DEBUG ---\n")
    return jsonify(result), 200


# GET /getjournaldata?uid=...&timestamp=...
@app.route('/getjournaldata', methods=['GET'])
def get_journal_data():
    uid = request.args.get('uid')
    timestamp = request.args.get('timestamp')
    if not uid or not timestamp:
        return jsonify({'message': 'uid and timestamp required'}), 400
    query = db.collection('journals').where('uid', '==', uid).where('timestamp', '==', timestamp).limit(1).stream()
    for doc in query:
        data = doc.to_dict()
        return jsonify({
            'uid': str(data.get('uid', "")),
            'name': str(data.get('name', "")),
            'message': str(data.get('message', "")),
            'timestamp': str(data.get('timestamp', "")),
            'image': str(data.get('image', "")) if data.get('image') is not None else ""
        }), 200
    return jsonify({'message': 'Journal not found'}), 404

@app.route('/deletejournal', methods=['DELETE'])
def delete_journal():
    journal_id = request.args.get('journal_id')
    if not journal_id:
        return jsonify({'status': False, 'message': 'journal_id required'}), 400

    db = firestore.client()
    doc_ref = db.collection('journals').document(journal_id)
    if not doc_ref.get().exists:
        return jsonify({'status': False, 'message': 'Journal not found'}), 404

    doc_ref.delete()
    return jsonify({'status': True, 'message': 'Journal deleted successfully'}), 200

# PUT /editjournal
@app.route('/editjournal', methods=['PUT'])
def edit_journal():
    print("[DEBUG] /editjournal called")

    # Required query parameters
    uid = request.args.get('uid')
    journal_id = request.args.get('journal_id')

    if not uid or not journal_id:
        return jsonify({'status': False, 'message': 'uid and journal_id are required as query parameters'}), 400

    # Optional update fields from form-data
    name = request.form.get('name')
    message = request.form.get('message')

    db = firestore.client()
    doc_ref = db.collection('journals').document(journal_id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({'status': False, 'message': 'Journal entry not found'}), 404

    journal_data = doc.to_dict()
    if journal_data.get('uid') != uid:
        return jsonify({'status': False, 'message': 'Unauthorized: uid mismatch'}), 403

    update_data = {}

    if name:
        update_data['name'] = name
    if message:
        update_data['message'] = message

    # Check if a valid image file is included
    image_file = None
    for k in request.files:
        if k.strip() == 'image':
            image_file = request.files[k]
            break

    if image_file:
        print("[DEBUG] Image file received")
        if allowed_file(image_file.filename):
            image_url = upload_image_to_firebase(image_file, uid)
            update_data['image'] = image_url
        else:
            return jsonify({'status': False, 'message': 'Invalid image file'}), 400

    if not update_data:
        return jsonify({'status': False, 'message': 'No updates provided'}), 400

    update_data['timestamp'] = datetime.now(timezone.utc).isoformat()
    doc_ref.update(update_data)

    print("[DEBUG] Journal updated:", update_data)
    return jsonify({'status': True, 'message': 'Journal updated successfully'}), 200

# Helper function: Classify category
def classify_category(step1, step2, step3):
    categories = ["anxiety", "couples", "crisis", "depression", "family", "trauma","Generic","wellness"]
    text = f"Step1: {step1}\nStep2: {step2}\nStep3: {step3}"

    prompt = f"""
    Classify the following user input into one of these therapy categories: {categories}.
    Return only the best category in JSON format:
    Example: {{"category": "anxiety"}}
    
    User Input:
    {text}
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    try:
        result = json.loads(response.choices[0].message["content"])
    except:
        result = {"category": "anxiety"}

    return result["category"]

@app.route("/therapy-response", methods=["GET", "POST"])
def therapy_response():
    if request.method == "GET":
        user_id = request.args.get("user_id")
        step1 = request.args.get("step1")
        step2 = request.args.get("step2")
        step3 = request.args.get("step3")
    else:
        data = request.get_json(force=True)
        user_id = data.get("user_id")
        step1, step2, step3 = data.get("step1"), data.get("step2"), data.get("step3")

    # Classify and fetch bot data as before...


    # Step 1: Classify the message
    category = classify_category(step1, step2, step3)

    # Step 2: Fetch bot data directly from document
    doc_ref = db.collection("ai_therapists").document(category).get()
    if not doc_ref.exists:
        return jsonify({"error": f"No bot found for category {category}"}), 404
    
    bot_data = doc_ref.to_dict()

    # Step 3: Return the response (no confidence)
    return jsonify({
        "user_id": user_id,
        "session_id": str(uuid.uuid4()),
        "bot_id": category,  # doc id is the category
        "bot_name": bot_data.get("name"),
        "preferred_style": bot_data.get("preferred_style", "balanced"),
        "color": bot_data.get("color"),
        "icon": bot_data.get("icon"),
        "image": bot_data.get("image")
    })

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from google.cloud import firestore


BOTS = ["Ava", "Sage", "Phoenix", "Raya", "River", "Jordan"]
SOS_MESSAGE = (
    "I'm really sorry you're feeling this way. Please reach out to a crisis line "
    "or emergency support near you or you can reach out to our SOS services. "
    "You're not alone in this. 💙"
)




# In-memory SOS counts
sos_counts = {}

@app.route("/sos", methods=["GET"])
def increment_sos():
    """Increment SOS count for a specific user."""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing 'user_id' parameter"}), 400

    # Increment SOS count for this user
    sos_counts[user_id] = sos_counts.get(user_id, 0) + 1
    return jsonify({
        "user_id": user_id,
        "sos_count": sos_counts[user_id]
    })


@app.route("/api/wellness", methods=["GET"])
def wellness_status():
    """Calculate Wellness Status based on recent check-ins and SOS usage."""
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing 'user_id' parameter"}), 400

        # Get SOS count for the user (default 0 if not found)
        sos_usage = sos_counts.get(user_id, 0)

        # Fetch check-ins from Firestore
        checkins_ref = db.collection("recent-checkin").where("uid", "==", user_id)
        docs = checkins_ref.stream()

        checkins = []
        for doc in docs:
            data = doc.to_dict()

            # normalize date
            try:
                formatted_date = datetime.strptime(
                    data.get("date", ""), "%d-%m-%Y"
                ).strftime("%Y-%m-%d")
            except Exception:
                formatted_date = data.get("date", "")

            checkins.append({
                "date": formatted_date,
                "mood": data.get("mood", ""),
                "intensity_raw": data.get("intensity", ""),  # keep original string
            })

        # --- Metrics ---
        low_mood_labels = {"sad", "tired", "angry", "anxious", "okay"}

        # 1) Low mood days (unique dates with low mood + low intensity)
        low_mood_dates = set(
            c["date"]
            for c in checkins
            if c["mood"].lower() in low_mood_labels and str(c["intensity_raw"]).lower() == "low"
        )
        low_mood_days = len(low_mood_dates)

        # 2) Convert intensity for numeric calculations
        for c in checkins:
            c["intensity"] = convert_intensity(c["intensity_raw"])

        # 3) Mood variety (unique moods)
        mood_variety = len(set(c["mood"].lower() for c in checkins if c["mood"]))

        # 4) Average mood (numeric intensity)
        avg_mood = round(sum(c["intensity"] for c in checkins) / len(checkins), 1) if checkins else 0

        # 5) Recovery rate (low → high within 2 days)
        recovery_count = 0
        for i, c in enumerate(checkins):
            if c["mood"].lower() in low_mood_labels and str(c["intensity_raw"]).lower() == "low":
                try:
                    current_date = datetime.strptime(c["date"], "%Y-%m-%d")
                except Exception:
                    continue
                for next_c in checkins[i+1:]:
                    try:
                        next_date = datetime.strptime(next_c["date"], "%Y-%m-%d")
                    except Exception:
                        continue
                    if 0 < (next_date - current_date).days <= 2 and next_c["intensity"] >= 6:
                        recovery_count += 1
                        break

        recovery_rate = round((recovery_count / low_mood_days) * 100, 1) if low_mood_days > 0 else 100

        # --- Scoring ---
        score = 0
        if mood_variety >= 8: score += 10
        if low_mood_days < 5: score += 20
        if sos_usage == 0: score += 20
        if avg_mood >= 6: score += 20
        if recovery_rate >= 66: score += 30

        # --- Status ---
        if score >= 90:
            status = "THRIVING"
            message = "✅ Excellent mental health indicators! You're maintaining emotional variety, zero crisis episodes, and consistent positive trends."
        elif score >= 70:
            status = "STABLE"
            message = "🙂 You're doing well overall, but there’s room for improvement. Keep tracking and maintaining positive habits."
        else:
            status = "NEEDS ATTENTION"
            message = "⚠ Your metrics show some concerning trends. Consider using available support tools and tracking progress."

        return jsonify({
            "user_id": user_id,
            "average_mood": avg_mood,
            "low_mood_days": low_mood_days,
            "mental_health_status": status,
            "message": message,
            "mood_variety": mood_variety,
            "recovery_rate": recovery_rate,
            "score": score,
            "sos_usage": sos_usage
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def convert_intensity(intensity):
    """Convert intensity string to numeric scale 1–10."""
    mapping = {"low": 3, "medium": 6, "high": 9}
    if isinstance(intensity, int):
        return intensity
    return mapping.get(str(intensity).strip().lower(), 5)  # default = 5



if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")

 





















































































































































































