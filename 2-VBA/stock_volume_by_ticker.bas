Attribute VB_Name = "Module1"
Sub stock_volume_by_ticker():
    Dim ws As Worksheet
    
    For Each ws In Worksheets
    ' set datatypes for variables
        Dim TickerRow As Double
        Dim StockVolume As Double
        Dim TotalRows As Double
        Dim VolumeRow As Double

    
    'Get total number of rows
        TotalRows = Cells(Rows.Count, 1).End(xlUp).Row
    ' Assign cell I1 with Ticker symbol label and cell J1 with Total Stock Volume label
        Range("I1").Value = "Ticker"
        Range("J1").Value = "Total Stock Volume"
    ' Initialize StockVolume and VolumeRow
        StockVolume = 0
        VolumeRow = 2
        
        For TickerRow = 2 To TotalRows
    
    ' Check if we are still within the same Ticker symbol, if it is not...
            If (Cells(TickerRow, 1).Value <> Cells(TickerRow + 1, 1).Value) Then
                
                ' 9th column holds Ticker summary
                Cells(VolumeRow, 9).Value = Cells(TickerRow, 1).Value
                
                ' Add to the StockVolume total
                StockVolume = StockVolume + Cells(TickerRow, 7).Value
                
                ' 10th column holds StockVolume summary
                Cells(VolumeRow, 10).Value = StockVolume
                
                ' Add one to the VolumeRow
                VolumeRow = VolumeRow + 1
                ' Reset StockVolume total
                StockVolume = 0
    
    'If cell immediately following a row is the same Ticker symbol...
            Else
                
                ' Add to the StockVolume total
                StockVolume = StockVolume + Cells(TickerRow, 7).Value
            
            End If
        Next TickerRow
        
    
    Next ws
        

End Sub
