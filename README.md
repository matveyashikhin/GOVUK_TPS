# GOVUK-Trademark-Scrape

### We will be trying to create a Flask app that provides a simple one-stop-shop interface for interacting with the data on GOVUKs trademark office website journals.

### There is a mix of Python and Apple Shortcuts (this is used to bypass the government websites cloudfare security which renders Selenium and Beautiful Soup useless in scraping).

### Having gone through some iteration (thanks Claude), the current app looks better and is also now hosted on PythonAnywhere 

https://matvash.pythonanywhere.com/

<img width="1394" alt="Screenshot 2025-06-24 at 21 25 17" src="https://github.com/user-attachments/assets/79f0f90c-2672-4d94-8158-8689f9d56fff" />

The goal is to add patents into this and provide a framework (backtested) for identifying Filing Driven Signals (Trademark Pending XD) as was hypothesised in some of the following papers (consider the below a sort of literature review)

https://pubsonline.informs.org/doi/10.1287/mnsc.2020.3887 

_The findings suggest that investors systematically undervalue new trademark registrations, particularly when faced with complexity and uncertainty. This undervaluation persists despite trademarks representing commercially viable products/services where technical uncertainty has been resolved, though market acceptance uncertainty remains. The research highlights trademarks as an important but understudied form of intellectual property that contributes substantially to firm value but is not efficiently priced by the market._

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4280505

_This paper develops a novel, market‐based measure of the value of individual trademarks—an intangible asset historically understudied relative to patents—by quantifying the stock‐market reaction to trademark publication. It links 1.3 million trademarks from the USPTO to 18,867 U.S. publicly traded firms (1961–2021) and estimates each mark’s dollar value via abnormal returns around its publication._

https://www.tandfonline.com/doi/full/10.1080/13662716.2019.1685374#d1e2082

_"Looking at the between-effects row in Table 5, it can be seen that patents and/or trademarks have significant effects on the market valuation in the selected industries. Again, this result highlights the importance to investors of benchmarking corporate IPR portfolios when making the investment decisions. In fact, in the Computer and Automobile industries, only the between differences seems to matter. In other words, in these industries, the markets seem to grant higher premiums to the companies that seem relatively more innovative than their competitors (between-effects), rather than rewarding a premium to any additional innovation assets from a company (within-effects). Nevertheless, significant differences emerge across the industries and depending on the IPR or their combination: i) in the Computer industry, both patents and trademarks are significantly valued by the markets; ii) only patents are effective for Automobile companiesFootnote21 and; iii) for Pharmaceutical companies, only trademarks show significant between-effects. For the Automobiles companies, the results of this study would thus not contradict the earlier work of Malmberg who suggests that these companies may still not prefer trademarks (only) to protect their new products (Malmberg Citation2005). Regarding the pharmaceuticals industry, where the within variations matter, the results suggest a lesser importance of benchmarking the patenting activity of companies. The fast development of generic or alternative drugs have certainly influenced the trend in this industry, making the implementation of strong differentiation strategies even more fundamental, for instance through massive investments in trademarks-protected brands and other marketing assets."_
