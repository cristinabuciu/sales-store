# sales-store
1. [x] Authentification Service:

    - pt login username:cristina parola:cristina
    - [x] login 
    - [x] logout 
    - [x] register 
    - [x] validateCredentials 
    
2. [ ] StockService
    
    - [x] getStock  
    - [x] getStockById 
    - [x] getStockByName 
    - [x] updateStock 
    - [ ] sendStock ?
    - [ ] processStock ?
    
3. [x] OrderService

    -tab nou Order in care facem comenzi (refolosim Add purchase)

    - [x] placeOrder
    - [x] proccessOrder
    - [x] updateOrder
    
4. [ ] ReportService
    
    - [ ] getReportByTimeRange
    - [ ] getCustomReport
    - [ ] getCustomerReport
    - [x] getStockReport
    - [x] getOrderReport
    - [x] getUsersReport
    - [ ] sendReport
    
5. [ ] CustomerRequestService
    
    - [x] sendCustomerRequest
    - [x] porcessCustomerRequest
    
6. [ ] RecommendationService

    - [ ] getCustomerRemmendation
    - [ ] getRecommendation
    - [ ] sentRecommendation
    - [ ] processRecommendation

To deploy on localhost please run:

```bash
./script.sh # this will build the images
docker-compose up --build # to start the containers
docker-compose down # might consider using this
```

in browser -> http://localhost:3003/
