# build model...
library(xgboost)
library(tidyverse)

features <- read_csv("feature-engineering/feature_df.csv") 
features$label <- factor(features$label)
#features$id <- 1
#features$did <- 1

# create train val split
ind <- sample(1:nrow(features), 0.7*nrow(features))
train <- features[ind,]
val <- features[-ind,]

dfeats <- xgb.DMatrix(as.matrix(select(features, -label)), label = as.matrix(select(features, label)))
dmodel <- xgb.DMatrix(as.matrix(select(train, -label)), label = as.matrix(select(train, label)))
dvalid <- xgb.DMatrix(as.matrix(select(val, -label)), label = as.matrix(select(val, label)))

test_eval <- function(y_prob, dtrain) {
  y_true <- getinfo(dtrain, "label")
  best_precision <- MLmetrics::Precision(y_true, y_prob, positive="1")
  best_recall <- MLmetrics::Recall(y_true, y_prob, positive="1")
  weight = 0.5
  Fscore_weighted <- ((1+weight*weight) * (best_precision * best_recall))/((weight*weight*best_precision)+best_recall)
  return(list(metric="MCC", value=Fscore_weighted))
}

param <- list(objective = "multi:softmax", 
              num_class = 2, 
              eta = 0.01, 
              max_depth = 4,
              min_child_weight = 3,
              subsample = 0.8,
              colsample_bytree = 0.8,
              base_score = 0.005,
              eval_metric = test_eval,
              maximize = TRUE)

xgb_model <- xgb.train(data = dmodel, param, nrounds = 20,
                       watchlist = list(mod = dmodel, val = dvalid))

caret::confusionMatrix(predict(xgb_model, dfeats), features$label)

