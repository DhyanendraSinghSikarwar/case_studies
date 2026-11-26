# Chapter 20 answer key: Clocks and Calendars

All results were recomputed by script (exact fractions for clock times, Python's calendar for dates).

## Self-check answers
1. At 9:00 the hour hand is at 270° and the minute hand at 0° (the 12). The gap is 270°, which is more than 180°, so the angle is 360 - 270 = **90°**. Formula: |30 × 9 - 0| = 270, then 360 - 270 = 90.
2. **No.** 2100 ends in 00, so it is a century year. Century years are leap years only if divisible by 400. 2100 divided by 400 is 5.25, so 2100 is not a leap year.
3. 15 days = 2 full weeks (14 days) + 1 day. Only the remainder 1 matters: Tuesday + 1 = **Wednesday**.

## Practice answers

**Q1.** Hour hand at 8 × 30 = 240°, minute hand at 0°. The gap is 240°, above 180°, so 360 - 240 = **120°**.

**Q2.** The minute hand does a full 360° in 60 minutes: 360 / 60 = **6° per minute**. The hour hand does 360° in 12 hours = 720 minutes: 360 / 720 = **0.5° per minute**.

**Q3.** Hour hand: 30 × 5 + 0.5 × 30 = 165°. Minute hand: 6 × 30 = 180°. Gap = 180 - 165 = **15°**. Formula check: |150 - 165| = 15.

**Q4.** At 12:20, H = 12 counts as 0 on the dial. Hour hand: 0 + 0.5 × 20 = 10°. Minute hand: 6 × 20 = 120°. Gap = 120 - 10 = **110°**. Formula check with H = 0: |0 - 5.5 × 20| = 110.

**Q5.** 150 days: 150 / 7 = 21 weeks (147 days) with remainder 3. Going back 3 days from Tuesday: Monday (1), Sunday (2), **Saturday** (3). Python check: Saturday.

**Q6.** Rule: divisible by 4, but centuries must be divisible by 400.
- 1800: century, 1800 / 400 = 4.5, **not** a leap year.
- 2024: 2024 / 4 = 506, not a century, **leap year**.
- 2400: century, 2400 / 400 = 6, **leap year**.
- 2500: century, 2500 / 400 = 6.25, **not** a leap year.
Answer: **2024 and 2400**.

**Q7.** Days left in March after the 10th: 31 - 10 = 21 (this reaches 31 March). Then 25 more days in April. Total = 21 + 25 = **46 days**.

**Q8.** True time passed: 6 hours. The clock gains 2 minutes each hour, so it gains 6 × 2 = 12 minutes. It shows 6:00 pm + 12 minutes = **6:12 pm**.

**Q9.** 4 January + 30 days: January has 31 days, so 4 January + 27 days = 31 January, and 3 more days reach **3 February 2027**. Weekday: 30 = 4 weeks (28 days) + 2. Monday + 2 = **Wednesday**. So the answer is Wednesday 3 February 2027.

**Q10.** Hour hand: 30 × 9 + 0.5 × 12 = 276°. Minute hand: 6 × 12 = 72°. Gap = 276 - 72 = 204°, above 180°, so 360 - 204 = **156°**. Formula check: |270 - 66| = 204, then 156.

**Q11.** Hour hand: 30 × 1 + 0.5 × 48 = 54°. Minute hand: 6 × 48 = 288°. Gap = 288 - 54 = 234°, so 360 - 234 = **126°**. Formula check: |30 - 264| = 234, then 126.

**Q12.** At 2:00 the hour hand is 60° ahead. The minute hand gains 5.5° per minute. Time = 60 / 5.5 = 120/11 = 10 and 10/11 minutes. Answer: **2:10 and 10/11 minutes (about 2:10:55)**.

**Q13.** At 7:00 the hour hand is 210° ahead of the minute hand. The hands are opposite when the gap is 180°, so the gap must shrink from 210° to 180°. The minute hand must gain 210 - 180 = 30°. Time = 30 / 5.5 = 60/11 = 5 and 5/11 minutes. Answer: **7:05 and 5/11 minutes (about 7:05:27)**. Check: hour hand at 210 + 0.5 × 5.4545 = 212.73°; minute hand at 6 × 5.4545 = 32.73°; difference 180°.

**Q14.** True time passed: 6 hours. The clock loses 5 minutes each hour, so it loses 6 × 5 = 30 minutes. It shows 3:00 pm - 30 minutes = **2:30 pm**.

**Q15.** 26 November to 31 December: 4 days left in November (30 - 26) plus 31 days of December = 35 days. 35 = 5 weeks exactly, remainder 0. The weekday is the same: **Thursday**. (Python calendar: 31 Dec 2026 is a Thursday.)

**Q16.** 30 days = 4 full weeks (28 days) + 2 extra days. Every full week contains one Sunday, so 4 Sundays. The month starts on Saturday, so the 2 extra days (the 29th and 30th) are Saturday and Sunday. That gives one more Sunday. Total = **5 Sundays**.

**Q17.** From 20 January: 11 days remain in January (31 - 20), reaching 31 January. February (2027, 28 days): total 39. Remaining 60 - 39 = 21 days, so the date is **21 March 2027**. Weekday: 60 = 8 weeks (56 days) + 4. 20 January 2027 is a Wednesday (1 January 2027 is a Friday, 19 days later: 19 = 2 weeks + 5, Friday + 5 = Wednesday). Wednesday + 4 = **Sunday**. Python check: Sunday 21 March 2027. (A weekend due date: a finance team would need a rule for it.)

**Q18.** At 5:00 the hour hand is 150° ahead. The hands are 40° apart in two situations:
- Before they meet: the gap has shrunk from 150° to 40°. The minute hand gains 110°. Time = 110 / 5.5 = **20 minutes**, so 5:20.
- After they pass each other: the minute hand is 40° ahead. It must gain 150 + 40 = 190°. Time = 190 / 5.5 = 380/11 = **34 and 6/11 minutes**, so 5:34 and 6/11 minutes.
Check 5:20: hour hand 160°, minute hand 120°, gap 40°. Check 5:34 6/11: hour hand 150 + 17.27 = 167.27°, minute hand 6 × 34.545 = 207.27°, gap 40°.

**Q19.** The clock shows correct time on a 12-hour dial when its total gain is a whole multiple of 12 hours = 720 minutes (the first time is exactly 720). At 4 minutes per hour: 720 / 4 = 180 true hours. 180 hours = 7 days + 12 hours (7 × 24 = 168, remainder 12). Starting from midnight at the start of Sunday, that is **12:00 noon on the following Sunday, after 7 and a half days**. At that moment the clock has run 180 + 12 = 192 hours (exactly 8 days), so it shows 12:00 on its dial; the true time is 12:00 noon, which looks the same on a 12-hour dial.

**Q20.** The hands form a right angle when the gap is 90° or 270° (equivalent on the circle). The gap changes by 5.5° per minute, starting at 0° at midnight. The gap equals 90 + 360k or 270 + 360k at times t = (90 + 360k) / 5.5 or (270 + 360k) / 5.5 minutes. Counting those times inside 0 to 1440 minutes gives 44 (the gap goes through 1440 × 5.5 = 7920° in a day, which is 22 full turns, and each turn passes the 90° and 270° marks once). Answer: **44 times** (22 in each 12 hours). Script check by exact fractions: 44.

**Q21.** 1 January to 29 February 2028 (a leap year, so February has 29 days): January has 31 days, so 1 January + 31 days = 1 February, and 28 more days reach 29 February. Total 59 days. 59 = 8 weeks (56 days) + 3. Saturday + 3 = Sunday (1), Monday (2), **Tuesday** (3).

**Q22.** From 14 February 2025, 400 days later: 400 days = 365 + 35. One year later is 14 February 2026 (no 29 February falls between these two dates, so that year has 365 days). Then 35 more days: February 2026 has 28 days, so 14 Feb + 14 days = 28 Feb; 21 more days reach **21 March 2026**. Weekday: 400 = 57 weeks (399 days) + 1, so one day after the weekday of 14 February 2025. 14 February 2025 was a Friday, so the maturity day is **Saturday**. Python check: 21 March 2026, Saturday. Financial year (April to March): 21 March 2026 is before 1 April 2026, so it belongs to **FY 2025-26**.

**Q23.** Days from 1 January 2000 to 1 January 2026: 26 years. Leap years inside (2000, 2004, 2008, 2012, 2016, 2020, 2024) are 7. Days = 26 × 365 + 7 = 9490 + 7 = 9497. 9497 / 7 = 1356 weeks (9492 days) with remainder 5. Going back 5 days from Thursday: Wednesday (1), Tuesday (2), Monday (3), Sunday (4), **Saturday** (5). So 1 January 2000 was a **Saturday**.

**Q24.** Weekday of the 13th of each month, 2027. 13 January: 1 January is Friday, 12 days later is Friday + 5 (12 = 7 + 5) = Wednesday. Each next month's 13th shifts forward by the previous month's length mod 7 (31 gives +3, 30 gives +2, 28 gives +0):
- Jan 13: Wednesday. Feb 13: +3 = Saturday. Mar 13: +0 = Saturday. Apr 13: +3 = Tuesday. May 13: +2 = Thursday. Jun 13: +3 = Sunday. Jul 13: +2 = Tuesday. Aug 13: +3 = **Friday**. Sep 13: +3 = Monday. Oct 13: +2 = Wednesday. Nov 13: +3 = Saturday. Dec 13: +2 = Monday.
Only **August 2027** has a Friday the 13th. Script check: [8].

**Q25.** A mirror reflects each hand's position left to right. The mirror reading and true time add up to 12:00 on a 12-hour dial (12:00 minus the shown time). 12:00 - 8:20: borrow an hour: 11:60 - 8:20 = **3:40**. Check: true 3:40 has the hour hand at 110° and the minute hand at 240°. In a mirror these become 360 - 110 = 250° and 360 - 240 = 120°. 250° on the dial is between 8 and 9 (8:20 position, 250 / 30 = 8.33) and 120° is the 20-minute mark. So the mirror shows 8:20, which matches.
