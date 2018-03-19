require(dplyr)
require(rgdal)
require(tidyr)
require(RColorBrewer)

# Leitura de Dados
nota_op <- read.csv('nota_opin.csv', header = TRUE, sep = ",")
head(nota_op$marca_ant)


## Mapas 
# Recomendação 
require(rgdal)
require(spdep)

bras <- readOGR('./Mapa', 
                layer = "Brasil",
                encoding = "Latin1")

# Extract unique IDS
unique_op <-
  nota_op %>% 
  group_by(ID) %>%
  select(ano, estado, marca_atual, marca_ant, carro_atual, carro_ant, carro_sub) %>% 
  summarise(ano = unique(ano),
            estado = unique(estado),
            marca_atual = unique(marca_atual), 
            marca_ant = unique(marca_ant),
            carro_atual = unique(carro_atual), 
            carro_sub = unique(carro_sub),
            carro_ant = unique(carro_ant))

sort(table(unique_op$estado))
sort(table(unique_op$marca_atual))
sort(table(unique_op$marca_ant))
sort(table(unique_op$carro_atual))
sort(table(unique_op$carro_ant))

# Notas Por estado 
# Filtrar Acima de Avaliações
recom_estado <-
  nota_op %>% 
  filter(marca_atual %in% c("Chevrolet", "Volkswagen", "Renault", "Fiat", "Hyundai") 
         & quesito == "Recomendação") %>% 
  group_by(estado, quesito, marca_atual) %>% 
  summarise(media_nota = round(mean(nota),2)) %>% 
  # Transformar em wide /
  spread(., marca_atual, media_nota)

bras@data <- 
  bras@data %>% 
  left_join(recom_estado, by = c("UF" = "estado"))

require(mapview)
# bras@data

png("brasil.png", height = 700, width = 900)
spplot(bras, 
        c("Chevrolet", "Fiat", "Renault", "Volkswagen", "Hyundai"), 
       at = seq(0, 10, 2),
       col.regions = brewer.pal(5, "Greens"))
dev.off()

n_estado_marca <- 
    unique_op %>% 
    filter(marca_atual %in% c("Chevrolet", "Volkswagen", "Renault", "Fiat", "Hyundai")) %>% 
    select(estado, marca_atual) %>% 
    group_by(estado, marca_atual) %>% 
    count()
  
  n_estado <- 
    unique_op %>% 
    filter(marca_atual %in% c("Chevrolet", "Volkswagen", "Renault", "Fiat", "Hyundai")) %>% 
  group_by(estado) %>% 
  count()

n_marca_atual <- 
  unique_op %>% 
  filter(marca_atual %in% c("Chevrolet", "Volkswagen", "Renault", "Fiat", "Hyundai")) %>% 
  group_by(marca_atual) %>% 
  count()

# Unir Base de Dados
n_junto <- 
  n_estado_marca %>% 
  left_join(n_estado, by = "estado") %>%
  left_join(n_marca_atual, by = "marca_atual") %>% 
  mutate(perc_estado = n.x/n.y,
         perc_marca = n.x/n) 

# Add dado região
n_junto <- 
  bras@data %>% 
  select(UF, REGIAO) %>% 
  right_join(n_junto, by = c("UF" = "estado"))

n_junto %>% 
  # filter(class == 1) %>% 
  ggplot(aes(x = UF, y = perc_estado, fill = marca_atual)) +  
  geom_bar(stat = 'identity', color = "black") +
  theme_bw() + 
  coord_flip() +
  facet_wrap(~REGIAO, scales = 'free_y') +
  scale_y_continuous(labels = scales::percent) +
  labs(fill = "") +
  geom_text(aes(label = n.x), color = "black",
            size = 4, position = position_stack(vjust = 0.5)) +
  scale_fill_brewer(palette = "Set2")
  
# Transição de Marca
# nota_op$marca_ant
# nota_op$marca_atual

# Preferências Carros Primeiro
unique_op %>% 
  filter(marca_ant == "Primeiro") %>% 
  group_by(marca_atual) %>% 
  count()

# Transição de Marca

n_change <- unique_op %>% 
  filter(marca_ant != "Primeiro") %>%
  select(marca_ant, marca_atual) 

n_change$trans <- as.character(n_change$marca_ant) == as.character(n_change$marca_atual)
n_change$junto <- paste(n_change$marca_ant,  n_change$marca_atual)

# Qtde de Transição
qte_marca_atual <- n_change %>%
  group_by(marca_atual) %>% 
  count()

# Marcas Anteriores = Marcas Atuais
total_junto <- n_change %>% 
  filter(marca_ant != "Dono")%>%
  filter(trans == TRUE)%>%
  group_by(junto) %>%
  count() %>% 
  arrange(desc(n))

total_junto$junto <- 
  total_junto$junto %>% 
  stringr::word(.,1) 

total_junto %>% 
  left_join(qte_marca_atual, by = c("junto" = "marca_atual")) %>% 
  mutate(perc = n.x/n.y) %>% 
  arrange(desc(perc)) %>% 
  ggplot(aes(x = reorder(junto, perc), y = perc, fill = junto)) +
  geom_bar(stat = 'identity') +
  coord_flip() +
  labs(y = "Porcentagem", x = "Marcas", fill = '') +
  theme_bw() +
  theme(axis.title.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank()) +
  scale_y_continuous(labels = scales::percent)


  

