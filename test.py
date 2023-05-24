from model.calculate_all_models import  calculate_all_models
from model.convert_to_lime import plot_lime_models
plot_lime_models("AAL",tarih= '2023-02-01',useTrend=False,news_model=False,delay=2)
