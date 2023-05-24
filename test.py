from model.calculate_all_models import  calculate_all_models
from model.convert_model_to_shap import plot_shap_models
plot_shap_models("AAL",tarih= '2023-02-01',useTrend=True,news_model="news_score_model1",delay=2)
