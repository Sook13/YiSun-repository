# 导入必要的库
library(plotly)
library(dplyr)

# 读取数据
data <- read.csv("EIB202_out.csv", header = TRUE)

# 将基因ID设置为行名
rownames(data) <- data$ID
data <- data[, -1]  # 删除ID列

# 获取每个基因的预测最高概率对应的分泌系统
predicted_system <- apply(data, 1, function(x) {
  max_prob <- max(x)
  if (max_prob >= 0.98) {   # 调整阈值到0.9
    return(names(x)[which.max(x)])
  } else {
    return("Non")
  }
})

# 将预测的分泌系统添加到数据框中
data$Predicted_System <- predicted_system

# 重新设置数据框的行名为基因ID
data$ID <- rownames(data)

# 将数据转换为适用于plotly的格式
plot_data <- data %>%
  select(ID, Predicted_System) %>%
  mutate(Predicted_System = factor(Predicted_System)) %>%
  group_by(Predicted_System) %>%
  mutate(x = row_number(), y = rnorm(n())) %>%
  ungroup()

# 绘制交互式的三维散点图
p <- plot_ly(plot_data, x = ~x, y = ~y, z = ~Predicted_System, color = ~Predicted_System, type = "scatter3d", mode = "markers", text = ~ID) %>%
  layout(scene = list(xaxis = list(title = "Gene ID"), yaxis = list(title = "Random Y"), zaxis = list(title = "Predicted Secretion Proteins")))

# 标出指定的基因ID
highlight_genes <- c("ETAE_1616", "ETAE_3059", "ETAE_3060", "ETAE_0256")
highlight_data <- plot_data %>%
  filter(ID %in% highlight_genes)

p <- add_trace(p, data = highlight_data, x = ~x, y = ~y, z = ~Predicted_System, color = I("red"), type = "scatter3d", mode = "markers+text", text = ~ID, textposition = "top center", name = "Selecteded Genes")

p
