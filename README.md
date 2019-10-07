## **Predicting NFL Player Compensation**
Updated on 10/06/19

---

## Summary  
I created a linear regression model to predict the compensation for NFL players based on past game performance and previous contract sizes.  The goal is to project the compensation for a player to find who is being underpaid / overpaid or to project the contract size for an upcoming free agent player.

---

## Key Components and Assumptions

**Years for analysis = 1994 to 2019**
> The NFL salary cap was established in 1994 as a way to keep teams balanced.  Starting at $34 million in 1994, the cap has steadily increased every year to the current limit of $188 million in 2019.*  My analysis of salaries will start in 1994 because prior to the salary cap player salaries were much less consistant.  
> 
> \* There was technically no salaray cap due to ongoing negotiations related to player benefits (CBA agreement).  At the time teams opporated as if the prior year cap was in place because they knew once negotiations were complete the salary cap would be official again.


**Pct of Cap = Player Compensation / Salary Cap**

> To compare players across different time periods, compensation is converted to "Pct of cap", which is  the player's compensation for a given year divided by the salary cap of the same year.  A player making up 10% of a team's cap in 1994 should be comparable to a player making up 10% of the cap in 2019.  Most players make up less than 5% of a team's salary cap, but superstars can account for almost 16% in some cases.
> 
> A reasonable question is why don't we just inflation adjust the dollars instead of dividing by the salary cap.  The reason is the NFL salary cap increases faster than the rate of inflation, modern players would always seem more expensive on average (see below).
>
> ![salary_cap](./images/salary_cap.png)

**Player Compensation = Annual salary + relevant bonuses**

> NFL player contracts consist of an annual salary (typically the largest part) and a combination of bonuses such as a signing bonus, workout bonus, roster bonus, and/or others.  Bonus money can be spread out over multiple years, which can be especially useful for teams close to their salary cap limit and who cannot affort a large cost in the current year.  As a result, when looking at a player's compensation, this will include all components of salaries and bonuses for the year.  Below is Eli Manning's most recent contract for example.
> ![eli_manning](./images/eli_manning_contract.png)

**Players in scope are Quarterbacks (QBs), Running Backs (RBs), and Wide Recievers (WRs)**

> The only players I will be focusing on are QBs, RBs, and WRs.  This is becuase these positions have the most game stats associated with them (sorry offenseive lineman).  In the future I may be able to expand to additional positions with the avalibility of additional positional statistics.

---

## Data Collection 
There are 2 data sources for this project:
 1. **spotrac.com:** Details about player contracts for each year.
  
 2. **pro-football-reference.com:**  Gameplay statistics for all NFL players who have ever played in the NFL

---

## Modeling


## Results