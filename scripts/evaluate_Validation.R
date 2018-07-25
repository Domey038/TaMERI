#Library initializations
suppressMessages(library("data.table"))
suppressMessages(library(magrittr))
suppressMessages(library(tidyr))
suppressMessages(library(ggplot2))
suppressMessages(library(stringr))
suppressMessages(library(gridExtra))

#----------------------------------------#
#             Preprocessing              #
#----------------------------------------#
#Commandline input
args = commandArgs(trailingOnly=TRUE)
if (length(args) != 1) {
  print("")
  stop("Required input:\n<TaMERI/data/>")
}

#DEBUG - START
args <- c("/home/domey/Studium-Shit/Master/SS_2018/Masterarbeit/working_dir/TaMERI/data/results_RF")
#DEBUG - END

#Parameter
data_set <- "homo_sapiens"
ML_algorithm <- "Random Forest"

#List all cross-validation folds in the data directory
folds <- list.files(args[1], pattern="cv\\.fold_.*\\.tsv") %>%
  strsplit(., "\\.") %>%
  as.data.table(.) %>%
  .[2,] %>%
  unlist(.)

#Create "plots" directory in working directory
invisible(ifelse(!dir.exists("plots"), dir.create("plots"), FALSE))

#Initialize dt_complete (which contains the validation results of all cross-validation folds)
cv_dt <- data.table()

#Combine the fold results into one table
for (fold in folds){
  #Read results
  path <- file.path(args[1], paste("cv", fold, "tsv", sep="."))
  results <- fread(path, sep="\t", header=TRUE)
  #Add a fold column to the results table
  results[, fold:=fold]
  #Add to combined data frame
  cv_dt <- rbind(cv_dt, results)
}

#Plot simple obs vs pred Scatterplot
plotVS <- ggplot(cv_dt, aes(real, pred, col=fold)) + 
  geom_point() + 
  geom_abline() + 
  facet_wrap(~ fold, scale="free") + 
  theme(legend.position="none") +
  xlab("TM/EM ER ratio - Observed") + 
  ylab("TM/EM ER ratio - Predicted") + 
  ggtitle("5-fold cross-validation of TaMERI", 
          paste(paste("ML algorithm:", ML_algorithm, sep=" "),
                paste("Data set:", data_set, sep=" "), sep="\n"
          ))
outputPath = file.path("plots",
                       paste("predictive_power", "scatterplot", "png", sep="."))
png(outputPath, 1600,1200, res=180)
suppressWarnings(print(plotVS))
out <- dev.off()

#Preprocessing for trend accuracy
cv_cons_dt <- cv_dt[, .(real_cons=real>0, pred_cons=pred>0, fold)]
table(cv_cons_dt[,c("real_cons","pred_cons")])

#Preprocessing for accuracy vs cutoff
ae <- cv_dt[, .(absolute_error=real-pred, fold=fold)]
calc_accuracy <- function(cutoff, df){
  acc <- df[, .(accuracy=sum(absolute_error<=cutoff)/.N, abs_error_cutoff=cutoff), by=fold]
  return(acc)
}
diff_cutoffs <- seq(0, max(abs(ae$absolute_error)/2), max(abs(ae$absolute_error))/100)
acc_df <- lapply(diff_cutoffs, calc_accuracy, ae) %>%
  rbindlist(.)

#Plot accurcy vs absolute error cutoff
plotAcc <- ggplot(acc_df, aes(abs_error_cutoff, accuracy, col=fold)) + 
  geom_line(size=1) +   
  geom_vline(xintercept=0.0025, linetype="dashed", col="black") + 
  scale_x_continuous(limits=c(0,0.03),
                     breaks = round(seq(0, 0.03, by = 0.0025),4)) + 
  scale_y_continuous(limits=c(0.4,1.0),
                     breaks = round(seq(min(acc_df$accuracy), 1.0, by = 0.05), 1)) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) + 
  xlab("Absolute error cutoff") + 
  ylab("Accuracy") + 
  ggtitle("5-fold cross-validation of TaMERI", 
          paste(paste("ML algorithm:", ML_algorithm, sep=" "),
                paste("Data set:", data_set, sep=" "), sep="\n"
                ))
outputPath = file.path("plots",
                       paste("predictive_power", "accuracy", "png", sep="."))
png(outputPath, 1600,1200, res=220)
suppressWarnings(print(plotAcc))
out <- dev.off()

#Combine both plots into a single one
outputPath = file.path("plots",
                       paste("validation", "png", sep="."))
png(outputPath, 1600,1600, res=220)
suppressWarnings(grid.arrange(plotVS, plotAcc, heights=c(2,1)))
out <- dev.off()
