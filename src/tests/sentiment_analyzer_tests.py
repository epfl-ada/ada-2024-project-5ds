import sys
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/models')
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/scripts')
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/data')
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/utils')
from dataloader import load_initial_dataset
from sentiment_analysis_plots import get_sentiment_from_dataframe
from sentiment_analysis import get_sentiment_string
from loading_utils import save_dataframe_to_csv
    
def test_get_sentiment():
    text = "I am happy."
    get_sentiment_string(text)  
    return True

def test_get_sentiment_from_plot(df, column_name):
    print("Entering test function")
    df = get_sentiment_from_dataframe(df, column_name)
    save_dataframe_to_csv(df, "plot_summaries.csv")
    return df.head(10)

movie, character, plot_summaries, tvtropes, name_clusters = load_initial_dataset("dataset")

print(test_get_sentiment_from_plot(plot_summaries, "Summary"))