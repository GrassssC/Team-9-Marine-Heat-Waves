mhws_onshore = read.csv("Rottnest_Island_onshore_biased_analys.csv",header = TRUE,colClasses=c("numeric","Date","Date","numeric","Date","numeric","numeric","numeric"))
mhws_offshore = read.csv("Rottnest_Island_offshore_biased_analys.csv",header = TRUE,colClasses=c("numeric","Date","Date","numeric","Date","numeric","numeric","numeric"))


onshore_duration = mhws_onshore$duration
onshore_c_int = mhws_onshore$cumulative_intensity
onshore_max_int = mhws_onshore$max_intensity
onshore_mean_int = mhws_onshore$mean_intensity

offshore_duration = mhws_offshore$duration
offshore_c_int = mhws_offshore$cumulative_intensity
offshore_max_int = mhws_offshore$max_intensity
offshore_mean_int = mhws_offshore$mean_intensity

summary(onshore_c_int)
summary(onshore_duration)
summary(onshore_max_int)
summary(onshore_mean_int)

summary(offshore_c_int)
summary(offshore_duration)
summary(offshore_max_int)
summary(offshore_mean_int)

boxplot(onshore_c_int,main="onshore cumulative intensity")
boxplot(onshore_c_int,outline = FALSE,main="onshore cumulative intensity outliers removed")

boxplot(onshore_duration,main="onshore duration")
boxplot(onshore_duration,outline=FALSE,main="onshore duration outliers removed")

boxplot(onshore_max_int,main="onshore max intensity")
boxplot(onshore_max_int,outline=FALSE,main="onshore max intensity outliers removed")

boxplot(onshore_mean_int,main="onshore mean intensity")
boxplot(onshore_mean_int,outline=FALSE,main="onshore mean intensity outliers removed")




boxplot(offshore_c_int,main="offshore cumulartive intensity")
boxplot(offshore_c_int,outline=FALSE,main="offshore cumulartive intensity outliers removed")

boxplot(offshore_duration,main="offshore duration")
boxplot(offshore_duration,outline=FALSE,main="offshore duration outliers removed")

boxplot(offshore_max_int,main="offshore max intensity")
boxplot(offshore_max_int,outline=FALSE,main="offshore max intensity outliers removed")

boxplot(offshore_mean_int,main="offshore mean intensity")
boxplot(offshore_mean_int,outline=FALSE,main="offshore mean intensity outliers removed")