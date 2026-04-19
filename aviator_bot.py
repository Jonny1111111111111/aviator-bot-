# Aviator Paper Trading Bot - Bet9ja

# Strategy: Enter on streak 11+, 2.5x progression, cashout at 2x

from playwright.sync_api import sync_playwright
import time, json, os, requests
from datetime import datetime

TELEGRAM_TOKEN = os.getenv(TELEGRAM_TOKEN)
TELEGRAM_CHAT  = os.getenv(TELEGRAM_CHAT)

def tg(msg):
if TELEGRAM_TOKEN and TELEGRAM_CHAT:
try:
requests.post(
f”https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage”,
json={“chat_id”: TELEGRAM_CHAT, “text”: msg},
timeout=5
)
except:
pass

STARTING_BALANCE = 5000
BASE_BET         = 200
ENTRY_STREAK     = 11
CASHOUT_TARGET   = 2.0
BET_MULTIPLIER   = 2.5
MAX_BET          = 3050
BET9JA_URL       = “https://sports.bet9ja.com/casino”

PROGRESSION = []
bet = BASE_BET
for i in range(5):
PROGRESSION.append(min(round(bet), MAX_BET))
bet *= BET_MULTIPLIER
if bet > MAX_BET:
break

print(f”Progression: {PROGRESSION}”)

class AviatorBot:
def **init**(self):
self.balance      = STARTING_BALANCE
self.streak       = 0
self.in_cycle     = False
self.cycle_step   = 0
self.cycle_staked = 0
self.history      = []
self.cycles       = []

```
def log(self, msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def process_round(self, multiplier):
    is_under = multiplier < CASHOUT_TARGET
    self.history.append(multiplier)

    if is_under:
        self.streak += 1
    else:
        self.streak = 0

    self.log(f"Round: {multiplier:.2f}x | Streak: {self.streak} | Balance: N{self.balance:,.0f}")

    if self.in_cycle:
        bet_amount = PROGRESSION[self.cycle_step]

        if not is_under:
            self.balance += bet_amount
            self.cycle_staked += bet_amount
            net = self.balance - STARTING_BALANCE
            msg = (f"WIN | Step {self.cycle_step+1} | Bet N{bet_amount} | "
                   f"Profit N{bet_amount} | Net P&L N{net:+,.0f} | Bal N{self.balance:,.0f}")
            self.log(msg)
            tg(msg)
            self.cycles.append({"result":"WIN","step":self.cycle_step+1,
                                "profit":bet_amount,"balance":self.balance})
            self.in_cycle = False
            self.cycle_step = 0
            self.cycle_staked = 0
            self.streak = 0

        else:
            self.balance -= bet_amount
            self.cycle_staked += bet_amount
            self.cycle_step += 1
            self.log(f"Loss step {self.cycle_step} | Bet N{bet_amount} | Bal N{self.balance:,.0f}")

            if self.cycle_step >= len(PROGRESSION):
                msg = f"BUST | Total staked N{self.cycle_staked} | Bal N{self.balance:,.0f}"
                self.log(msg)
                tg(msg)
                self.cycles.append({"result":"BUST","profit":-self.cycle_staked,"balance":self.balance})
                self.in_cycle = False
                self.cycle_step = 0
                self.cycle_staked = 0

    elif not self.in_cycle and self.streak >= ENTRY_STREAK:
        self.in_cycle = True
        self.cycle_step = 0
        self.cycle_staked = 0
        msg = f"ENTERING CYCLE | Streak: {self.streak} | First bet: N{PROGRESSION[0]}"
        self.log(msg)
        tg(msg)

def print_summary(self):
    wins  = [c for c in self.cycles if c["result"] == "WIN"]
    busts = [c for c in self.cycles if c["result"] == "BUST"]
    total = sum(c["profit"] for c in self.cycles)
    print("="*50)
    print(f"Rounds: {len(self.history)} | Cycles: {len(self.cycles)}")
    print(f"Wins: {len(wins)} | Busts: {len(busts)}")
    print(f"P&L: N{total:+,.0f} | Balance: N{self.balance:,.0f}")
    print("="*50)
    tg(f"Session ended | Wins: {len(wins)} | Busts: {len(busts)} | P&L: N{total:+,.0f} | Bal: N{self.balance:,.0f}")

def run(self):
    self.log("Starting Aviator Paper Trading Bot...")
    tg("Aviator bot started")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,
            args=["--no-sandbox","--disable-setuid-sandbox","--disable-dev-shm-usage"])
        context = browser.new_context(viewport={"width":1280,"height":800})
        page    = context.new_page()

        self.log("Opening Bet9ja...")
        page.goto(BET9JA_URL, timeout=30000)
        page.wait_for_timeout(5000)

        self.log(f"Watching for streak {ENTRY_STREAK}+...")
        last_rounds = []

        try:
            while True:
                try:
                    rounds = page.evaluate("""
                        () => {
                            const selectors = [
                                '.paycoef','.bubble-multiplier',
                                '[class*="coefficient"]','[class*="multiplier"]',
                                '[class*="coef"]','[class*="history"]'
                            ];
                            for (const sel of selectors) {
                                const els = document.querySelectorAll(sel);
                                if (els.length > 0) {
                                    return Array.from(els)
                                        .map(el => el.innerText.trim().replace('x','').replace(',','.'))
                                        .filter(v => !isNaN(parseFloat(v)))
                                        .map(v => parseFloat(v))
                                        .slice(0, 30);
                                }
                            }
                            return [];
                        }
                    """)

                    if rounds and rounds != last_rounds:
                        new_rounds = []
                        if last_rounds:
                            for r in rounds:
                                if r not in last_rounds[:3]:
                                    new_rounds.append(r)
                        else:
                            new_rounds = rounds[:5]

                        for r in reversed(new_rounds):
                            self.process_round(r)

                        last_rounds = rounds

                except Exception as e:
                    self.log(f"Error: {e}")

                time.sleep(3)

        except KeyboardInterrupt:
            self.log("Stopping...")
            self.print_summary()
            browser.close()
```

if **name** == “**main**”:
bot = AviatorBot()
bot.run()
