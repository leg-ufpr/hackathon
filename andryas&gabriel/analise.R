# Andryas Waurzenczak                                         17/03/2018
# ----------------------------------------------------------------------
# Biblioteca
# ----------------------------------------------------------------------
library(RColorBrewer)
library(ggplot2)
library(fmsb)
library(dplyr)
library(ggradar)
library(mcglm)
library(Matrix)
library(reshape2)
# ----------------------------------------------------------------------
# Leitura dos dados
# ----------------------------------------------------------------------
dt <- read.csv("nota_opin.csv")
## marca_atual
dt[, 22] <- tolower(dt[, 22])
## carro_atual
dt[, 24] <- tolower(dt[, 24])

# ----------------------------------------------------------------------
# Não usado
# ----------------------------------------------------------------------
# ## Qt characters pros
# dt$npros <- nchar(as.character(dt$pros))
# dt$npros <- cut(dt$npros, breaks = c(0, 50, 100, 150, 200, 10000))
# 
# ## Qt characters contra
# dt$ncontra <- nchar(as.character(dt$contra))
# dt$ncontra <- cut(dt$ncontra, breaks = c(0, 50, 100, 150, 200, 10000))
# 
# # Base com km 0 retirada
# dt2 <- dt %>%
#     filter(km > 0)
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Somente quesitos,  notas,  estados, marca, carro
# Nota format long
nota <- melt(dt[, c(1:16, 21, 22, 24)],  id.vars =
    c("ID", "carro_atual", "estado", "marca_atual"))
nota$nota <- as.numeric(nota$value)

# Nota 2 format wide
nota2 <- dt[, c(1:16, 21, 22, 24)]

# ----------------------------------------------------------------------
# Análise exploratoria dos dados
# ----------------------------------------------------------------------

# Acabamento-Câmbio-Consumo-Custo Beneficio-Desempenho
png("prop1.png",  height = 700,  width = 900)
ggplot(subset(nota,  variable %in% levels(variable)[1:5]),
       aes(x = nota,  y = marca_atual)) +
    geom_bar(aes(y = ..prop..), fill  = "dodgerblue2") +
    facet_grid(~variable) + labs(x = "",  y = "Frequência")
dev.off()

png("prop2.png",  height = 700,  width = 900)
# Estabilidade-Estilo-Freios-Instrumentos-Interior
ggplot(subset(nota,  variable %in% levels(variable)[6:10]),
       aes(x = nota)) +  geom_bar(aes(y = ..prop..), fill  = "dodgerblue2") +
    facet_grid(~variable) + labs(x = "",  y = "Frequência")
dev.off()

png("prop3.png",  height = 700,  width = 900)
# Motor-Porta malas-Posição de dirigir-Recomendação-Suspensão
ggplot(subset(nota,  variable %in% levels(variable)[11:15]),
       aes(x = nota)) +  geom_bar(aes(y = ..prop..), fill  = "dodgerblue2") +
    facet_grid(~variable) + labs(x = "",  y = "Frequência")
dev.off()

# ----------------------------------------------------------------------
# Gráfico radar
# ----------------------------------------------------------------------
notaradar <- aggregate(nota ~ variable + marca_atual, data = nota,  FUN = mean)

notaradar <-  dcast(notaradar, marca_atual ~ variable)

rownames(notaradar) <- notaradar$marca_atual

notaradar <- notaradar[, -1]

notaradar <- rbind(rep(10, 15), rep(0, 15), notaradar)

# Geral
png("radarplot.png", width = 900, height = 700)
# display.brewer.all()
radarchart(notaradar,pcol = palette())
legend(x=1.5, y=0.75, legend = rownames(notaradar[-c(1,2),]), bty = "n", pch=20,
       col= palette() , text.col = "grey", cex=1.2, pt.cex=3) 
dev.off()

    
# ----------------------------------------------------------------------
# Qual a diferença entre as marcas por quesitos
dt3 <- nota2[, -1]
dt3 <- cbind(dt3[, 1:15] / 10, dt3[, c(16:18)])

quesitos <- colnames(dt3)[-c(ncol(dt3):16)]

formulas <- lapply(1:15, function(x)
    as.formula(paste0(quesitos[x],"~ marca_atual")))

m0 <- mcglm(c(formulas), matrix_pred =
                             list(mc_id(dt3),mc_id(dt3),
                                  mc_id(dt3),mc_id(dt3),
                                  mc_id(dt3),mc_id(dt3),
                                  mc_id(dt3),mc_id(dt3),
                                  mc_id(dt3),mc_id(dt3),
                                  mc_id(dt3),mc_id(dt3),
                                  mc_id(dt3),mc_id(dt3),
                                  mc_id(dt3)
                                  ),
            variance = rep("binomialP"),
            link = rep("logit", 15))


# ----------------------------------------------------------------------
# Ajuste quesitos agrupados
dt4 <- read.csv("novos_quesitos.csv")
dt4 <- aggregate(nota ~ quesito + marca_atual + ID, data = dt4[, c(1, 2, 3, 9)],
          FUN = mean)
dt5 <- dcast(dt4, ID +   marca_atual  ~ quesito)

# ----------------------------------------------------------------------
modelo <- readRDS("modelo.RData")

modelo$mu_list[4]

names(modelo)

x <- summary(modelo, response = c(4, 14, 3))

x$'Resp.Variable 3'
x$'Resp.Variable 4'
x$'Resp.Variable 14'

saveRDS(x, "summary.RData")

colnames(dt)[2:16]
