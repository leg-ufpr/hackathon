require(dplyr)
require(qdap)
# Leitura de Arquivos ----------------------------------------------------
require(jsonlite)

opinioes <- fromJSON("opinioes.json", flatten = TRUE)
opinioes <- data.frame(opinioes)
names(opinioes) <- c("id", "manchete", "modelo", "dono", "anterior", "pros", 
                     "contra", "defeitos", "opiniao", "data")
# Criar Variáveis ---------------------------------------------------------

## Tempo de Uso do Carro
opinioes$t_uso <- sub("\\-.*", "", opinioes$anterior) %>% 
  tidyr::extract_numeric(.)

## Km Rodados
library(qdap)
opinioes$km <- genXtract(opinioes$anterior, "-", ":") %>% 
  gsub("\\.", "", .) %>% 
  tidyr::extract_numeric()

## Marca Anterior
opinioes$marca_ant <-
  sub(".*:", "", opinioes$anterior) %>% 
  trimws() %>% 
  stringr::word(.,1)

## Carro antigo
opinioes$carro_ant <-
  sub(".*:", "", opinioes$anterior) %>% 
  trimws() %>%
  stringr::word(.,2)

## Ano Modelo
opinioes$ano <-
  opinioes$modelo %>% 
  as.character() %>% 
  stringr::word(.,-1)

# Marca Atual
opinioes$marca_atual <-
  opinioes$modelo %>% 
  as.character() %>% 
  gsub('[[:digit:]]+', '', .) %>% 
  gsub("|[|]|[|!|#|$|%|(|)|*|,|.|:|;|<|=|>|@|^|_|`|||~|.|{|}|]|/|", "", .) %>% 
  rm_white(.) %>% 
  stringr::word(.,1)

# Carro Atual
opinioes$carro_atual <-
  opinioes$modelo %>% 
  as.character() %>% 
  gsub('[[:digit:]]+', '', .) %>% 
  gsub("|[|]|[|!|#|$|%|(|)|*|,|.|:|;|<|=|>|@|^|_|`|||~|.|{|}|]|/|", "", .) %>% 
  rm_white(.) %>% 
  stringr::word(.,2)

# Tipo de Carro
opinioes$carro_sub <-
  opinioes$modelo %>% 
  as.character() %>% 
  gsub('[[:digit:]]+', '', .) %>% 
  gsub("|[|]|[|!|#|$|%|(|)|*|,|.|:|;|<|=|>|@|^|_|`|||~|.|{|}|]|/|", "", .) %>% 
  rm_white(.) %>% 
  stringr::word(.,3)

# Potência
# opinioes$carro_sub <-
  # opinioes$modelo %>%
  # as.character() %>%
  # # gsub('[[:digit:]]+', '', .) %>%
  # gsub("|[|]|[|!|#|$|%|(|)|*|,|.|:|;|<|=|>|@|^|_|`|||~|.|{|}|]|/|", "", .) %>%
  # rm_white(.) %>% 
  #   
  
  # stringr::word(.,4)


# Separar por Estado
opinioes$estado <- 
  opinioes$dono %>% 
  stringr::word(.,-1)

# # Cidade
# opinioes$estado <- 
#   opinioes$dono %>% 
#   stringr::word(.,-1)

# Tratamento Texto --------------------------------------------------------
rm_acento <- function(x) iconv(x, to = "ASCII//TRANSLIT")
stp_pt <- 
  tm::stopwords("pt") %>% 
  rm_acento()

texto <-
  opinioes %>%
  select(pros, contra, defeitos, opiniao) %>%
  apply(., 2, tolower) %>%
  apply(., 2, function(x) gsub("[][!#$%()*,.:;<=>@^_`|~.{}]", " ", x)) %>%
  apply(., 2, function(x) rm_acento(x)) %>% 
  apply(., 2, function(x) gsub('[[:digit:]]+', '', x)) %>%  
  as.character() %>% 
  purrr::map(~tm::removeWords(., stp_pt)) %>% 
  unlist() %>% 
  matrix(., 5329, 4) %>% 
  data.frame() %>% 
  plyr::rename(., c("X1"= "pros", "X2"= "contra", "X3"= "defeitos", "X4"= "opiniao")) %>% 
  apply(., 2, function(x) as.character(x)) 

texto <- 
  texto %>%
  data.frame() %>% 
  apply(., 2, function(x) rm_white(x))

opinioes[, c("pros", "contra", "defeitos", "opiniao")] <- texto

# names(opinioes) 
# Salvar Data.frame em csv
opinioes <- 
  opinioes %>% 
  select(id, ano, km, t_uso, dono, estado, marca_atual, marca_ant, 
         carro_atual, carro_sub, carro_ant, data,
         pros, contra, defeitos, opiniao)

# Unir Base de Dados
nota <- read.csv('notas.csv', header = TRUE, sep = ";")
head(nota)

nota_opin <- 
  nota %>% 
  left_join(opinioes, by = c('ID' = "id"))
head(nota_opin)
write.csv(x = nota_opin, 
          file = "nota_opin.csv", 
          fileEncoding = "utf8", 
          sep = ";",
          dec = ".",
          row.names = FALSE)