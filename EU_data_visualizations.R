# NOTE: This file generates descriptive health spending table

setwd("")
library(readxl)
library(dplyr)


# read raw data
total_spending_df <- read_excel("health_exp_ntl_currency.xlsx", sheet = "Sheet 1")
curative_spending_df <- read_excel("health_exp_ntl_currency.xlsx", sheet = "Sheet 2")
preventive_spending_df <- read_excel("health_exp_ntl_currency.xlsx", sheet = "Sheet 3")
immunization_spending_df <- read_excel("health_exp_ntl_currency.xlsx", sheet = "Sheet 4")


# clean raw data
col_names <- c("Country", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024")
eu_countries <- c(
  "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
  "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
  "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
  "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
  "Slovenia", "Spain", "Sweden"
)



total_spending_df <- total_spending_df[17:48,]
total_spending_df <- total_spending_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(total_spending_df) <- col_names
total_spending_df <- total_spending_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric)) %>%
  filter(Country %in% eu_countries)

curative_spending_df <- curative_spending_df[17:48,]
curative_spending_df <- curative_spending_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(curative_spending_df) <- col_names
curative_spending_df <- curative_spending_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric)) %>%
  filter(Country %in% eu_countries)

preventive_spending_df <- preventive_spending_df[17:48,]
preventive_spending_df <- preventive_spending_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(preventive_spending_df) <- col_names
preventive_spending_df <- preventive_spending_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric)) %>%
  filter(Country %in% eu_countries)

immunization_spending_df <- immunization_spending_df[17:48,]
immunization_spending_df <- immunization_spending_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(immunization_spending_df) <- col_names
immunization_spending_df <- immunization_spending_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric)) %>%
  filter(Country %in% eu_countries)

# fill in Ireland, Spain, Italy, Hungary, Netherlands, Portugal, and Slovakia using WHO data
immunization_who_df <- read_excel("Immunization expenditure 2026-05-02 15-55 UTC.xlsx", sheet = "Sheet1")
immunization_who_df <- immunization_who_df %>%
  filter(DESCRIPTION == "What is the government expenditure on vaccines used in routine immunization?") %>%
  filter(YEAR > 2014) %>%
  select(COUNTRYNAME, YEAR, VALUE)
colnames(immunization_who_df) <- c("Country", "Year", "Value")
immunization_who_df$Value[immunization_who_df$Value %in% c("NR", "ND")] <- NA
# fix names and add asterisks
immunization_who_df$Country[immunization_who_df$Country == "Netherlands (Kingdom of the)"] <- "Netherlands"
immunization_who_df$Value <- as.numeric(immunization_who_df$Value) / 1000000

immunization_who_clean_df <- data.frame(
  Country = unique(immunization_who_df$Country),
  `2015` = immunization_who_df$Value[immunization_who_df$Year == 2015],
  `2016` = immunization_who_df$Value[immunization_who_df$Year == 2016],
  `2017` = immunization_who_df$Value[immunization_who_df$Year == 2017],
  `2018` = immunization_who_df$Value[immunization_who_df$Year == 2018],
  `2019` = immunization_who_df$Value[immunization_who_df$Year == 2019],
  `2020` = immunization_who_df$Value[immunization_who_df$Year == 2020],
  `2021` = immunization_who_df$Value[immunization_who_df$Year == 2021],
  `2022` = immunization_who_df$Value[immunization_who_df$Year == 2022],
  `2023` = immunization_who_df$Value[immunization_who_df$Year == 2023],
  `2024` = immunization_who_df$Value[immunization_who_df$Year == 2024],
  check.names = FALSE
)

# add to immunization_spending_df
missing_countries <- immunization_who_clean_df$Country
immunization_spending_df <- immunization_spending_df %>%
  filter(!(Country %in% missing_countries))

immunization_spending_df <- rbind(immunization_spending_df, immunization_who_clean_df)






# normalize spending as percent of total health spending (make sure every df is in the correct order)
total_spending_df <- total_spending_df[order(total_spending_df$Country),]
preventive_spending_df <- preventive_spending_df[order(preventive_spending_df$Country),]
immunization_spending_df <- immunization_spending_df[order(immunization_spending_df$Country),]


preventive_spending_pcttotal_df <- preventive_spending_df
preventive_spending_pcttotal_df[,2:11] <- (preventive_spending_df[,2:11] / total_spending_df[,2:11]) * 100

immunization_spending_pcttotal_df <- immunization_spending_df
immunization_spending_pcttotal_df[,2:11] <- (immunization_spending_df[,2:11] / total_spending_df[,2:11]) * 100

immunization_spending_pctpreventive_df <- immunization_spending_df
immunization_spending_pctpreventive_df[,2:11] <- (immunization_spending_df[,2:11] / preventive_spending_df[,2:11]) * 100







#### preventable deaths ####
# contains rate per 100,000 population
preventable_deaths_df <- read_excel("hlth_cd_apr$defaultview_spreadsheet.xlsx", sheet = "Sheet 2")

# clean
preventable_deaths_df <- preventable_deaths_df[14:49,]
preventable_deaths_df <- preventable_deaths_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(preventable_deaths_df) <- col_names
preventable_deaths_df <- preventable_deaths_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric)) %>%
  filter(Country %in% eu_countries)

median(
  c(
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Belgium"],
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Cyprus"],
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Malta"],
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Portugal"],
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Romania"],
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Slovakia"]
  )
)

median(
  c(
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Estonia"],
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Finland"],
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Germany"],
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Italy"],
    preventable_deaths_df$`2024`[preventable_deaths_df$Country == "Netherlands"]
  )
)




##### Scatter plots #####

preventive_spending_realeuros <- read_excel("health_exp_2015_euros.xlsx", sheet = "Sheet 7")
populations <- read_excel("tps00001_page_spreadsheet.xlsx", sheet = "Sheet 1")


preventive_spending_realeuros <- preventive_spending_realeuros[17:53,]
preventive_spending_realeuros <- preventive_spending_realeuros %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(preventive_spending_realeuros) <- col_names
preventive_spending_realeuros <- preventive_spending_realeuros %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric)) %>%
  filter(Country %in% eu_countries)

preventive_spending_realeuros <- preventive_spending_realeuros[order(preventive_spending_realeuros$Country),]
preventive_spending_realeuros[,2:11] <- preventive_spending_realeuros[,2:11] * 1000000

populations <- populations[13:62,]
populations <- populations %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(populations) <- col_names
populations <- populations %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric)) %>%
  filter(Country %in% eu_countries)
populations <- populations[order(populations$Country), ]



preventive_spending_percapita <- cbind(
  preventive_spending_realeuros$Country,
  preventive_spending_realeuros[2:11] / populations[2:11]
)
colnames(preventive_spending_percapita) <- col_names




realGDP_percapita_df <- read_excel("real GDP per capita.xlsx", sheet = "Sheet 1")

realGDP_percapita_df <- realGDP_percapita_df[13:54,]
realGDP_percapita_df <- realGDP_percapita_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(realGDP_percapita_df) <- col_names
realGDP_percapita_df <- realGDP_percapita_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric)) %>%
  filter(Country %in% eu_countries)






####### GENERATE PLOTS #######
#### FLAG SCATTERPLOT ####
library(ggplot2)
library(tidyr)
library(dplyr)
library(patchwork)
library(ggimage)      # for geom_flag()
library(countrycode)  # for converting country names -> ISO2 codes

## RESHAPE DATA ----------------------------------------------------------
# All years
spending_long_all <- preventive_spending_percapita |>
  select(1:11) |>
  pivot_longer(cols = -Country, names_to = "Year", values_to = "Spending")
deaths_long_all <- preventable_deaths_df |>
  select(1:11) |>
  pivot_longer(cols = -Country, names_to = "Year", values_to = "Deaths")

# Pre-COVID years
spending_long_pre <- preventive_spending_percapita |>
  select(1:6) |>
  pivot_longer(cols = -Country, names_to = "Year", values_to = "Spending")
deaths_long_pre <- preventable_deaths_df |>
  select(1:6) |>
  pivot_longer(cols = -Country, names_to = "Year", values_to = "Deaths")

## JOIN DATA FRAMES ------------------------------------------------------
country_levels <- unique(preventive_spending_percapita$Country)

# ISO2 codes (lowercase, required by geom_flag) for each country
iso2_lookup <- tibble(
  Country = country_levels,
  iso2    = tolower(countrycode(country_levels, origin = "country.name", destination = "iso2c"))
)


combined_df  <- inner_join(spending_long_all, deaths_long_all, by = c("Country", "Year")) |>
  mutate(Country = factor(Country, levels = country_levels)) |>
  left_join(iso2_lookup, by = "Country")

combined_df2 <- inner_join(spending_long_pre, deaths_long_pre, by = c("Country", "Year")) |>
  mutate(Country = factor(Country, levels = country_levels)) |>
  left_join(iso2_lookup, by = "Country")

## PLOT BUILDER FUNCTION ------------------------------------------------
make_scatter <- function(data, y_var, y_label, title, flag_size = 0.025) {
  ggplot(data, aes(x = Spending, y = .data[[y_var]], image = iso2)) +
    geom_flag(size = flag_size) +
    labs(
      title = title,
      x = "Preventive health expenditure per capita (millions of 2015 euros)",
      y = y_label
    ) +
    theme_minimal(base_size = 14) +
    theme(
      plot.title       = element_text(size = 13, face = "bold"),
      legend.position  = "none",
      panel.background = element_rect(fill = "grey92", color = NA),
      plot.background  = element_rect(fill = "white", color = NA),
      panel.grid.major  = element_line(color = "grey80", linewidth = 0.4),
      panel.grid.minor  = element_blank()
    )
}

## BUILD PLOTS ----------------------------------------------------------
# Slightly smaller flags for plot (a) since it has 2x the points of plot (b)
p1 <- make_scatter(combined_df,  "Deaths", "Preventable deaths per 100,000 population",
                   "a. 2015–2024", flag_size = 0.030)
p2 <- make_scatter(combined_df2, "Deaths", "Preventable deaths per 100,000 population",
                   "b. 2015–2019 (pre-COVID)", flag_size = 0.038)

## BUILD CUSTOM FLAG LEGEND ----------------------------------------------
n_countries <- length(country_levels)
n_cols      <- 3
n_rows      <- ceiling(n_countries / n_cols)

legend_df <- iso2_lookup |>
  arrange(Country) |>
  mutate(
    col = rep(1:n_cols, length.out = n_countries),
    row = rep(n_rows:1, each = n_cols, length.out = n_countries)
  )

flag_offset <- 0.1   # fixed gap (in x-units) between flag and text start

legend_plot <- ggplot(legend_df, aes(x = col, y = row)) +
  geom_flag(aes(image = iso2), size = 0.1) +
  geom_text(
    aes(x = col + flag_offset, label = Country),
    hjust = 0,          # left-align starting exactly at col + flag_offset
    size  = 3.6
  ) +
  xlim(0.8, n_cols + 1.3) +
  theme_void(base_size = 14) +
  theme(plot.margin = margin(5, 5, 5, 5))

# legend_plot

## COMBINE WITH PATCHWORK -----------------------------------------------
# combined <- (p1 | p2)   # no legend needed — flags self-identify
# 
# combined

combined <- (p1 | p2) / legend_plot +
  plot_layout(heights = c(3, 1))   # scatterplots get more vertical space than the legend row

combined

ggsave(
  filename = "combined_scatterplots.png",
  plot     = combined,
  width    = 17,
  height   = 11,
  units    = "in",
  dpi      = 300
)








#### population-weighted mean line graphs - combined figure ####

library(ggplot2)
library(patchwork)

years <- as.character(2015:2024)

#--------------------------------------------------
# Calculate weighted means and min/max values
#--------------------------------------------------

summary_df <- data.frame(
  Year = as.numeric(years),
  
  # Preventive spending (% total)
  PrevMean = sapply(years, function(y)
    weighted.mean(
      preventive_spending_pcttotal_df[[y]],
      populations[[y]],
      na.rm = TRUE
    )),
  
  PrevMin = sapply(years, function(y)
    min(preventive_spending_pcttotal_df[[y]], na.rm = TRUE)),
  
  PrevMax = sapply(years, function(y)
    max(preventive_spending_pcttotal_df[[y]], na.rm = TRUE)),
  
  # Immunization spending (% total)
  ImmTotalMean = sapply(years, function(y)
    weighted.mean(
      immunization_spending_pcttotal_df[[y]],
      populations[[y]],
      na.rm = TRUE
    )),
  
  ImmTotalMin = sapply(years, function(y)
    min(immunization_spending_pcttotal_df[[y]], na.rm = TRUE)),
  
  ImmTotalMax = sapply(years, function(y)
    max(immunization_spending_pcttotal_df[[y]], na.rm = TRUE)),
  
  # Immunization spending (% preventive)
  ImmPrevMean = sapply(years, function(y)
    weighted.mean(
      immunization_spending_pctpreventive_df[[y]],
      populations[[y]],
      na.rm = TRUE
    )),
  
  ImmPrevMin = sapply(years, function(y)
    min(immunization_spending_pctpreventive_df[[y]], na.rm = TRUE)),
  
  ImmPrevMax = sapply(years, function(y)
    max(immunization_spending_pctpreventive_df[[y]], na.rm = TRUE))
)

#--------------------------------------------------
# Common theme
#--------------------------------------------------

common_theme <- theme_minimal() +
  theme(
    panel.grid.minor = element_blank(),
    
    axis.line.x = element_line(color = "black", linewidth = 0.6),
    axis.line.y = element_line(color = "black", linewidth = 0.6),
    
    axis.text = element_text(color = "black"),
    axis.title = element_text(color = "black"),
    
    plot.title = element_text(face = "bold"),
    
    legend.position = "bottom",
    legend.title = element_blank()
  )

#--------------------------------------------------
# Panel 1: Preventive spending (% total)
#--------------------------------------------------

p1 <- ggplot(summary_df, aes(x = Year)) +
  
  geom_ribbon(
    aes(
      ymin = PrevMin,
      ymax = PrevMax,
      fill = "Minimum–maximum range"
    ),
    alpha = 0.20
  ) +
  
  geom_line(
    aes(
      y = PrevMean,
      color = "Population-weighted mean"
    ),
    linewidth = 1.2
  ) +
  
  geom_point(
    aes(y = PrevMean),
    color = "navy",
    size = 2.5
  ) +
  
  scale_color_manual(
    values = c("Population-weighted mean" = "navy")
  ) +
  
  scale_fill_manual(
    values = c("Minimum–maximum range" = "navy")
  ) +
  
  scale_x_continuous(
    breaks = 2015:2024
  ) +
  
  coord_cartesian(
    ylim = c(0, max(summary_df$PrevMax, na.rm = TRUE))
  ) +
  
  labs(
    title = "Preventive health spending",
    y = "% of total health expenditure",
    x = NULL
  ) +
  
  common_theme +
  
  theme(
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank()
  )

#--------------------------------------------------
# Panel 2: Immunization spending (% total)
#--------------------------------------------------

p2 <- ggplot(summary_df, aes(x = Year)) +
  
  geom_ribbon(
    aes(
      ymin = ImmTotalMin,
      ymax = ImmTotalMax,
      fill = "Minimum–maximum range"
    ),
    alpha = 0.20
  ) +
  
  geom_line(
    aes(
      y = ImmTotalMean,
      color = "Population-weighted mean"
    ),
    linewidth = 1.2
  ) +
  
  geom_point(
    aes(y = ImmTotalMean),
    color = "navy",
    size = 2.5
  ) +
  
  scale_color_manual(
    values = c("Population-weighted mean" = "navy")
  ) +
  
  scale_fill_manual(
    values = c("Minimum–maximum range" = "navy")
  ) +
  
  scale_x_continuous(
    breaks = 2015:2024
  ) +
  
  coord_cartesian(
    ylim = c(0, max(summary_df$ImmTotalMax, na.rm = TRUE))
  ) +
  
  labs(
    title = "Immunization spending",
    y = "% of total health expenditure",
    x = NULL
  ) +
  
  common_theme +
  
  theme(
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank()
  )

#--------------------------------------------------
# Panel 3: Immunization spending (% preventive)
#--------------------------------------------------

p3 <- ggplot(summary_df, aes(x = Year)) +
  
  geom_ribbon(
    aes(
      ymin = ImmPrevMin,
      ymax = ImmPrevMax,
      fill = "Minimum–maximum range"
    ),
    alpha = 0.20
  ) +
  
  geom_line(
    aes(
      y = ImmPrevMean,
      color = "Population-weighted mean"
    ),
    linewidth = 1.2
  ) +
  
  geom_point(
    aes(y = ImmPrevMean),
    color = "navy",
    size = 2.5
  ) +
  
  scale_color_manual(
    values = c("Population-weighted mean" = "navy")
  ) +
  
  scale_fill_manual(
    values = c("Minimum–maximum range" = "navy")
  ) +
  
  scale_x_continuous(
    breaks = 2015:2024
  ) +
  
  coord_cartesian(
    ylim = c(0, max(summary_df$ImmPrevMax, na.rm = TRUE))
  ) +
  
  labs(
    title = "Immunization spending",
    y = "% of preventive health expenditure",
    x = "Year"
  ) +
  
  common_theme

#--------------------------------------------------
# Combine panels
#--------------------------------------------------


combined_mean_spending_figure <-
  (p1 / p2 / p3) +
  plot_layout(guides = "collect") &
  theme(
    legend.position = "bottom"
  )

combined_mean_spending_figure

ggsave(
  filename = "combined_mean_spending_figure.png",
  plot     = combined_mean_spending_figure,
  width    = 8,
  height   = 9,
  units    = "in",
  dpi      = 300
)



# preventive spending euros per capita
preventive_spending_euros_percapita_2023 <- preventive_spending_euros$`2023` / populations$`2023`
mean(preventive_spending_euros_percapita_2023)
min(preventive_spending_euros_percapita_2023)
max(preventive_spending_euros_percapita_2023)
preventive_spending_euros_pc_df <- data.frame(
  Country = preventive_spending_euros$Country,
  `2023` = preventive_spending_euros_percapita_2023
)












#### all classifications of healthcare expenditures in millions of Euros ####

all_df <- read_excel("hlth_sha11_hc__custom_21843707_spreadsheet.xlsx", sheet = "Sheet 1")
curative_df <- read_excel("hlth_sha11_hc__custom_21843707_spreadsheet.xlsx", sheet = "Sheet 2")
longterm_df <- read_excel("hlth_sha11_hc__custom_21843707_spreadsheet.xlsx", sheet = "Sheet 4")
medical_goods_df <- read_excel("hlth_sha11_hc__custom_21843707_spreadsheet.xlsx", sheet = "Sheet 6")
preventive_df <- read_excel("hlth_sha11_hc__custom_21843707_spreadsheet.xlsx", sheet = "Sheet 7")

immunization_spending_df <- read_excel("health_exp_ntl_currency.xlsx", sheet = "Sheet 4")


all_df <- all_df[10,]
all_df <- all_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(all_df) <- col_names
all_df <- all_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric))

curative_df <- curative_df[17:53,]
curative_df <- curative_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(curative_df) <- col_names
curative_df <- curative_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric)) %>%
  filter(Country %in% eu_countries)
curative_df <- data.frame(
  Country = "EU total",
  `2023` = sum(curative_df$`2023`, na.rm = TRUE)
)

longterm_df <- longterm_df[10,]
longterm_df <- longterm_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(longterm_df) <- col_names
longterm_df <- longterm_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric))

medical_goods_df <- medical_goods_df[10,]
medical_goods_df <- medical_goods_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(medical_goods_df) <- col_names
medical_goods_df <- medical_goods_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric))

preventive_df <- preventive_df[10,]
preventive_df <- preventive_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(preventive_df) <- col_names
preventive_df <- preventive_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric))


# calculate fractions
curative_frac <- curative_df$X2023 / all_df$`2023`[1]
longterm_frac <- longterm_df$`2023`[1] / all_df$`2023`[1]
medical_goods_frac <- medical_goods_df$`2023`[1] / all_df$`2023`[1]
preventive_frac <- preventive_df$`2023`[1] / all_df$`2023`[1]


# calculate fraction of preventive health spending attributed to immunization
immunization_df <- immunization_spending_df[17:53,]
immunization_df <- immunization_df %>%
  select(1,2,4,6,8,10,12,14,16,18,20)
colnames(immunization_df) <- col_names
immunization_df <- immunization_df %>%
  mutate(across(c(`2015`, `2016`, `2017`, `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`), as.numeric)) %>%
  filter(Country %in% eu_countries)
immunization_df <- data.frame(
  Country = "EU total",
  `2023` = sum(immunization_df$`2023`, na.rm = TRUE)
)

immunization_frac_preventive <- immunization_df$X2023[1] / preventive_df$`2023`[1]
immunization_frac_total <- immunization_df$X2023[1] / all_df$`2023`


