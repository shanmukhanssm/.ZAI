# SpringPad's Seasonality Indicator

**Paste the below code in TradingView Pine Editor**

**Steps:**
1. Go to in.tradingview.com and create an account
2. Copy the code below
3. Paste it in the Pine Editor in TradingView
4. Click "Add to chart"

---

## CODE

```pinescript
//@version=5
indicator("Seasonality Monthly v2.0", "Seasonality Monthly v2.0", format = format.volume)

if not timeframe.ismonthly and not timeframe.isdaily
    runtime.error("Please switch timeframe to either Daily or Monthly")

i_year_start = input(2000, "Start Year")
// i_method = input.string("time", "Method", options=["time","time_close"])
i_method = "time_close"
i_text_size = input.string(size.auto, "Text Size", [size.auto, size.tiny, size.small, size.normal, size.large, size.huge])

//--------------------------------------------------------Functions----------------------------------------------------
f_array_stats(array_) =>
    count_pos_ = 0
    count_neg_= 0
    count_ = 0
    sum_  = 0.0
    if not na(array_) and array.size(array_) > 0
        for i_ = 0 to array.size(array_) - 1
            elem_ = array.get(array_, i_)
            if not na(elem_)
                sum_ += elem_
                count_ += 1
                switch
                    elem_ > 0 => count_pos_ += 1
                    elem_ < 0 => count_neg_ += 1
    avg_ = count_ > 0 ? sum_ / count_ : 0.0
    [sum_, avg_, count_, count_pos_, count_neg_]
//-------------------------------------------------------------------------------------------------------------------
[year_, month_, chg_pct_] = request.security(syminfo.tickerid, "M", [year(time_close), month(time_close), nz(close/close[1]-1)], gaps = barmerge.gaps_on, lookahead = barmerge.lookahead_on )

var year_start_ = math.max(year_, i_year_start)
var no_years_ = year(timenow) - year_start_ + 1
var matrix<float> data_  =  matrix.new<float>(no_years_,13,na)
var table table_ = na
var text_color_ = color.white
var bg_color_ = color.gray

if year_ >= year_start_
    cur_val_ = nz(matrix.get(data_, year_-year_start_, month_-1))
    matrix.set(data_, year_-year_start_, month_-1, cur_val_ + chg_pct_)

if barstate.islast
    table_ := table.new(position.middle_center, 13, no_years_ + 7, border_width = 1)

    table.cell(table_, 0, 0, str.format("Seasonality Monthly Performance - {0}:{1}", syminfo.prefix, syminfo.ticker), text_color = text_color_, bgcolor = color.blue, text_size = i_text_size)
    table.merge_cells(table_, 0,0,12,0)
    row = 1
    table.cell(table_, 0, row, "Year", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 1, row, "Jan", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 2, row, "Feb", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 3, row, "Mar", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 4, row, "Apr", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 5, row, "May", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 6, row, "Jun", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 7, row, "Jul", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 8, row, "Aug", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 9, row, "Sep", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 10, row, "Oct", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 11, row, "Nov", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 12, row, "Dec", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)

    for row_ = 0 to no_years_ - 1
        table.cell(table_, 0, 2+row_, str.tostring(row_ + year_start_), text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
        for col_ = 0 to 11
            val_ = nz(matrix.get(data_, row_, col_),0.0)
            val_color_ = val_ > 0.0 ? color.green : val_ < 0.0 ? color.red : color.gray
            table.cell(table_, 1+col_, 2+row_, str.format("{0,number,###.##%}", val_), bgcolor = color.new(val_color_,80), text_color = val_color_, text_size = i_text_size)
            true

    //Aggregates
    row_ = no_years_ + 2
    table.cell(table_, 0, row_, "AVG", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 0, row_+1, "SUM", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 0, row_+2, "+ive", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    table.cell(table_, 0, row_+3, "WR", text_color = text_color_, bgcolor = bg_color_, text_size = i_text_size)
    for col_ = 0 to 11
        arr_ = matrix.col(data_, col_)
        [sum_, avg_, count_, count_pos_, count_neg_] = f_array_stats(arr_)
        val_color_ = sum_ > 0 ? color.green : sum_ < 0 ? color.red : color.gray
        table.cell(table_, 1+col_, row_, str.format("{0,number,###.##%}", avg_), bgcolor = color.new(val_color_,50), text_color = val_color_, text_size = i_text_size)
        table.cell(table_, 1+col_, row_+1, str.format("{0,number,###.##%}", sum_), bgcolor = color.new(val_color_,50), text_color = val_color_, text_size = i_text_size)
        table.cell(table_, 1+col_, row_+2, str.format("{0}/{1}", count_pos_, count_), bgcolor = color.new(val_color_,50), text_color = color.new(color.white, 50), text_size = i_text_size)
        table.cell(table_, 1+col_, row_+3, str.format("{0,number,#.##%}", count_pos_/count_), bgcolor = color.new(val_color_,50), text_color = color.new(color.white, 50), text_size = i_text_size)
        true
```

---

### How to Read the Seasonality Table:

The indicator displays a table on your chart showing:

- **Monthly % returns** per year in green (positive) or red (negative)
- **AVG** row: Average monthly return across all years
- **SUM** row: Cumulative return for that month across all years
- **+ive row**: Count of positive months / total months (e.g., "5/7" means 5 out of 7 years were positive)
- **WR row**: Win rate for that month (percentage of years with positive returns)

This helps identify which months are historically strong or weak for a specific stock or index — useful for timing entries.

**Note:** The indicator requires a daily or monthly timeframe chart.
