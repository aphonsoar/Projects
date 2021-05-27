Sys.setenv(LANG = "en")
#install.packages("googledrive")
#install.packages("googlesheets4")
#install.packages("tidyverse")
#install.packages("plotly")

require(googledrive)
require(googlesheets4)
require(tidyverse)
require(plotly)

#rm(Sheets, Abas_sheets, df_vazio, Celulares)
#rm(list=setdiff(ls(), "x"))

# Dados da planilha:
Sheets <- sheets_get("https://docs.google.com/spreadsheets/d/1HL80aBaZKlxVWtArgIdeOi4CBODC9HjAmV3Tnu5vVf4/edit")

# Abas do sheets com dados:
Tabs <- Sheets[["sheets"]][["name"]]
#Abas_sheets <- Abas_sheets[- c(1,2,3)] # Delete first three tabs
Tabs

Qtd_tabs <- strtoi(summary(Tabs)[1]) # Number of tabs in the sheets
Tabs_to_read <- Qtd_tabs-6 # Do no consider the last 6 tabs which are not going to be used
Tabs <- Tabs[c(1:Tabs_to_read)] # List tabs from the first until the last, desconsidering the last 6


# Create an empty dataframe
rm(df_data, df_data_i, i, df_data_agg, fig, fig2)
df_data <- data.frame('Data' = 0,
                      'Despesa' = 0,
                      'Tipo - D' = '',
                      'Receita' = 0,
                      'Tipo - R' = '',
                      'Movimento' = '',
                      'Histórico' = '',
                      'Saldo Dia' = 0)
#df_data$Data <- as.double(df_data$Data)

# Renaming columns
names(df_data)[names(df_data) == 'Tipo...D'] <- "Tipo - D"
names(df_data)[names(df_data) == 'Tipo...R'] <- "Tipo - R"
names(df_data)[names(df_data) == 'Saldo.Dia'] <- "Saldo Dia"


i <- 1
#seq <- 1
for (i in 1:summary(Tabs_to_read)[1]) {
  if (Tabs[i] %in% c('Jan', 'Fev', 'Mar', 'Abr') == TRUE) {
    df_data_i <- read_sheet(ss = Sheets, sheet = Tabs[i], col_names = TRUE, skip=0)
  }
  else {
    df_data_i <- read_sheet(ss = Sheets, sheet = Tabs[i], col_names = TRUE, skip=1)#, range= "'Mai'!2:1000")
  }
  
  cat(Tabs[i], 'Read!')
  cat(' ')
  
  # Adjust data types
  df_data_i <- df_data_i[1:8] # select just the first 8 columns
  df_data_i$Data <- as.double(df_data_i$Data)
  df_data_i$Receita <- as.double(df_data_i$Receita)
  df_data_i$`Saldo Dia` <- as.double(df_data_i$`Saldo Dia`)
  df_data_i$Despesa <- as.double(df_data_i$Despesa)
  
  df_data <- rbind(df_data, df_data_i)
  
  cat(Tabs[i], 'Inserted!')
}

# Discard the zero line without data:
df_data <- df_data %>%
  filter(Data != 0)
rm(df_data_i)

# Format of dataframes:
#sapply(Mai[1:8], typeof)
#sapply(df_data, typeof)
#sapply(df_data_i, typeof)

# Summary
#summary(Mai[1:8])
#summary(df_data)
#summary(df_data_1)

# Adjust date from Excel to date
df_data$Data <- as.Date(df_data$Data, origin = "1899-12-30")

# Aggregate:
#help("aggregate")
#rm(Mai_agg)
df_data_agg <- df_data %>%
  group_by(Data) %>%
  summarise(Count = n(),
            Net_value_day = max(`Saldo Dia`, na.rm=TRUE),
            Expense = sum(Despesa, na.rm=T),
            Revenue = sum(Receita, na.rm=T))

# Charts with Plotly: https://plotly.com/r/line-charts/
# Plot line chart:
rm(fig)
fig <- plot_ly(df_data_agg,
               x = df_data_agg$Data,
               y = df_data_agg$Net_value_day,
               type = 'scatter',
               mode = 'lines+markers')
fig


# Plot line and scatter charts
rm(fig2)
fig2 <- plot_ly(df_data_agg,
                x = df_data_agg$Data)
fig2 <- fig2 %>% add_trace(y = df_data_agg$Net_value_day,
                           text = df_data_agg$Net_value_day,
                           hovertemplate = paste('%{x}', '<br>Net value day: %{text:.2s}<br>'),
                           texttemplate = '%{y:.2s}', textposition = 'outside',
                           name = 'Net value day',
                           type = 'scatter',
                           mode = 'lines+markers',
                           color = I('darkblue'))
fig2 <- fig2 %>% add_trace(y = df_data_agg$Expense,
                           text = df_data_agg$Expense,
                           hovertemplate = paste('%{x}', '<br>Expense: %{text:.2s}<br>'),
                           texttemplate = '%{y:.2s}', textposition = 'outside',
                           name = 'Expense',
                           type = 'bar',
                           color = I('red'))
fig2 <- fig2 %>% add_trace(y = df_data_agg$Revenue,
                           text = df_data_agg$Revenue,
                           hovertemplate = paste('%{x}', '<br>Revenue: %{text:.2s}<br>'),
                           texttemplate = '%{y:.2s}', textposition = 'outside',
                           name = 'Revenue',
                           type = 'bar',
                           color = I('darkgreen'))

fig2