

import pandas as pd
import matplotlib.pyplot as plt



class Cleaning:
    file_path = ""
    def __init__(self, filepath):
        self.filepath = Cleaning.file_path
        self.data = pd.read_csv(filepath)


    
    def raw_clean_data_check(self):
        # printing out a sample of the raw data
        a = self.data.head(5)
        b = self.data.tail(5)
        # checking the summary information(shape datatypes variables)
        c = self.data.info()
        duplicate = self.data.duplicated().any()
        if duplicate:
            # print out the duplicated rows
            print(f"The duplicated rows are: \n\t{self.data[self.data.duplicated()]}")
            # removing the duplicates
            self.data.drop_duplicates(inplace=True)
        else:
            pass
        # from the analysis some variables are wrongly calculated
        self.data["cogs"] = self.data["Quantity"] * self.data["Unit price"] * 0.05
        self.data["Revenue"] = self.data["Quantity"] * self.data["Unit price"]
        self.data["gross income"] = self.data["Revenue"] - self.data["cogs"]
        self.data["gross margin percentage"] = ((self.data["Revenue"] - self.data["cogs"]) / self.data["Revenue"]) * 100
        # returning the necessary values
        return a, b, c, self.data    
        


class SummaryStatistics(Cleaning):
    def __init__(self, filepath):
        super().__init__(self, filepath)
    
    def summary_statistics(self):
        self.raw_clean_data_check()
        # checking summary stats for the floats and integer variables
        a = self.data.describe()
        b = self.data[
            ["Unit price", "Total", "Quantity", "Tax 5%", "cogs", "gross margin percentage", "gross income",
             "Rating"]].median()
        return a, b
    
    

class SupermarketSalesData(SummaryStatistics):
    def __init__(self, filepath):
        super().__init__(self, filepath)
    
    def summary_statistics(self):
        self.raw_clean_data_check()
        # checking summary stats for the floats and integer variables
        a = self.data.describe()
        b = self.data[
            ["Unit price", "Total", "Quantity", "Tax 5%", "cogs", "gross margin percentage", "gross income",
             "Rating"]].median()
        return a, b

    def question1(self):
        self.raw_clean_data_check()

        product_gender = self.data.groupby(["Gender", "Product line"])["Quantity"].count()
        fig, ax = plt.subplots(figsize=(6, 6))
        bars = self.data.unstack().plot(kind="bar", ax=ax)
        for bar in bars.containers:
            for rect in bar.patches:
                height = rect.get_height()
                ax.annotate(
                    f"{height:.0f}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom"
                )
        plt.title("Product Line Distribution by Gender")
        plt.xlabel("Product Line")
        plt.ylabel("Product Line Count")
        plt.tight_layout()
        plt.show()

        product_line = self.data.groupby("Product line")["Quantity"].count()
        fig, ax = plt.subplots(figsize=(6, 6))
        product_line.plot(kind="bar", color=["Yellow", "pink"], alpha=0.5)
        for rect in ax.patches:
            height = rect.get_height()
            ax.annotate(
                f'{height:.0f}',
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom"
            )
        plt.title("Product Sale")
        plt.xlabel("Product")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    def question2(self):
        self.raw_clean_data_check()

        gender_rating_comparison = self.data.groupby("Gender")["Rating"].agg(["mean", "median", "count"])
        fig, ax = plt.subplots(figsize=(6, 6))
        gender_rating_comparison.plot(kind="bar", subplots=False, ax=ax, color=["green", "red", "yellow"], alpha=0.5)
        for rect in ax.patches:
            height = rect.get_height()
            ax.annotate(
                f'{height:.0f}',
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom"
            )
        plt.title("Mean and Median Gender against Rating")
        plt.xlabel("Gender")
        plt.ylabel("Count/Mean/Median")
        plt.tight_layout()
        plt.show()

    def question3(self):
        self.raw_clean_data_check()
        branch_city_rating = self.data.groupby(["Branch", "City", "Customer type"])["Rating"].agg(["mean", "median", "count"])
        fig, ax = plt.subplots(figsize=(12, 16))
        bars = branch_city_rating.unstack().plot(kind="bar", ax=ax, alpha=0.7)
        plt.xlabel("Branch")
        plt.ylabel("Rating")
        for bar in bars.containers:
            for rect in bar.patches:
                height = rect.get_height()
                ax.annotate(
                   f'{height:.0f}',  
                     # Position of the annotation (center of the bar)
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     # Position of the text label relative to the annotation (3 points above)
                     xytext=(0, 3),  
                     # Offset points relative to text coordinates
                     textcoords="offset points",
                     # Horizontal alignment of the text
                     ha='center',
                     # Vertical alignment of the text
                     va='bottom'
                )
        plt.tight_layout()
        plt.show()

    def question4(self):
        # which city brings in the highest income for the company and the mean and median of the income generated by the genders
        self.raw_clean_data_check()
        city_gross = self.data.groupby("City")["gross income"].agg(["mean", "median", "count"])
        fig, ax = plt.subplots(figsize=(12, 12))
        bar = city_gross.unstack().plot(kind="bar", ax=ax, color=["red", "orange", "yellow", "pink", "blue"], alpha=0.5)
        plt.title("City Mean and Median Gross Income")
        plt.ylabel("Gross Income")
        plt.xlabel("City")
        for rect in ax.patches:
            height = rect.get_height()
            ax.annotate(
                f'{height:.0f}',
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom"
            )
        plt.tight_layout()    
        plt.show()
        # which city brings in the highest gross income
        city_gross = self.data.groupby("City")["gross income"].sum()
        fig, ax = plt.subplots(figsize=(12, 12))
        bar = city_gross.plot(kind="bar", ax=ax, color=["red", "orange", "yellow", "pink", "blue"], alpha=0.5)
        plt.title("City Gross Income Return")
        plt.ylabel("Gross Income")
        plt.xlabel("City")
        for rect in ax.patches:
            height = rect.get_height()
            ax.annotate(
                f'{height:.0f}',
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom"
            )
        plt.tight_layout()    
        plt.show()

    def question5(self):
        # The customer status of people in each city and what is their gender
        self.raw_clean_data_check()
        city_member_gender = self.data.groupby(["Gender", "Customer type", "City"]).size()
        fig, ax = plt.subplots(figsize=(12, 6))
        bar = city_member_gender.unstack().plot(kind="bar", ax=ax)
        for bars in bar.containers:
            for rect in bars.patches:
                height = rect.get_height()
                ax.annotate(
                    f"{height:.0f}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom"
                )
        plt.yscale("log")
        plt.tight_layout()
        plt.show()

    def question6(self):
        # what is the consumption quantity of products in each city
        self.raw_clean_data_check()
        city_productline = self.data.groupby(["City", "Product line"])["Quantity"].count()
        fig, ax = plt.subplots(figsize=(15, 13))
        bars = city_productline.unstack().plot(kind="bar", ax=ax)
        for bar in bars.containers:
            for rect in bar.patches:
                height = rect.get_height()
                ax.annotate(
                    f'{height:.0f}',  
                    # Position of the annotation (center of the bar)
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    # Position of the text label relative to the annotation (3 points above)
                    xytext=(0, 3),  
                    # Offset points relative to text coordinates
                    textcoords="offset points",
                    # Horizontal alignment of the text
                    ha='center',
                    # Vertical alignment of the text
                    va='bottom'
                )
        plt.tight_layout()
        plt.show()

    def question7(self):
        # Which gender are the highest consumers in each city which products do they buy
        self.raw_clean_data_check()
        gender_city_products = self.data.groupby(["Gender", "City", "Product line"])["Quantity"].count()
        fig, ax = plt.subplots(figsize=(12,6))
        bar = gender_city_products.unstack().plot(kind="bar", ax=ax)
        plt.ylabel("Quantity")
        for bars in bar.containers:
            for rect in bars.patches:
                height=rect.get_height()
                ax.annotate(
                    f"{height:.0f}",
                    xy = (rect.get_x()+rect.get_width()/2, height),
                    xytext = (0,3),
                    textcoords = "offset points",
                    ha = "center",
                    va = "bottom"
                )
        plt.tight_layout()        
        plt.show() 

    def question8(self):
        # Which city and gender pay the highest taxes
        self.raw_clean_data_check()
        gender_city_taxes = self.data.groupby(["Gender", "City"])["Tax 5%"].agg(["mean", "median", "count"])
        fig, ax = plt.subplots(figsize=(14,14))
        bar = gender_city_taxes.unstack().plot(kind="bar", alpha=0.6, ax=ax)
        plt.ylabel("Tax")
        for bars in bar.containers:
            for rect in bars.patches:
                height=rect.get_height()
                ax.annotate(
                    f"{height:.0f}",
                    xy = (rect.get_x()+rect.get_width()/2, height),
                    xytext = (0,3),
                    textcoords = "offset points",
                    ha = "center",
                    va = "bottom"
                )
        plt.tight_layout()        
        plt.show()  

    def question9(self):
        # what is the most preferred type of payment in each city and by which gender
        payment_city_gender = self.data.groupby(["City", "Gender", "Payment"]).size()
        fig, ax = plt.subplots(figsize=(30, 30))
        bar = payment_city_gender.unstack(level=0).plot(kind="pie", subplots=True, autopct='%1.1f%%', ax=ax)
        plt.ylabel("Count")
        plt.legend(prop={"size": 8}, loc="lower right")
        plt.tight_layout()
        plt.show()

    def question10(self):
        grossincome_gender = self.data.groupby("Gender")["gross income"].agg(["count", "median", "mean"])
        fig, ax = plt.subplots(figsize=(5,5))
        grossincome_gender.plot(kind="bar", ax=ax, color=["blue", "pink"], alpha=0.5)
        for rect in ax.patches:
            height = rect.get_height()
            ax.annotate(
                f'{height:.0f}',
                xy=(rect.get_x()+rect.get_width()/2, height),
                xytext=(0, 3),
                textcoords="offset points", 
                ha="center", 
                va="bottom"
            )
        plt.ylabel("Gross Income")   
        plt.tight_layout()
        plt.show() 
