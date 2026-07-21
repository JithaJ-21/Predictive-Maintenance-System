import os
import pandas as pd
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Circle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_FILE = os.path.join(BASE_DIR,"data","machine_log.csv")

GRAPH_DIR = os.path.join(BASE_DIR,"graphs")

def add_page_number(canvas, total_pages):
    page_num = canvas.getPageNumber()

    canvas.setFont("Helvetica", 9)

    canvas.setStrokeColor(colors.lightgrey)

    canvas.setLineWidth(0.5)

    canvas.line(
        15*mm,
        15*mm,
        195*mm,
        15*mm
    )


    canvas.setStrokeColor(colors.black)

    canvas.drawString(
        15*mm,
        10*mm,
        "Industrial Predictive Maintenance Report"
    )

    canvas.drawCentredString(
        105*mm,
        10*mm,
        datetime.now().strftime("%d-%m-%Y %H:%M")
    )

    canvas.drawRightString(
        195*mm,
        10*mm,
        f"Page {page_num} of {total_pages}"
    )

class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)

        for state in self._saved_page_states:
            self.__dict__.update(state)
            add_page_number(self, num_pages)
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)

def generate_pdf():
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=40,
        bottomMargin=40
    )

    df = pd.read_csv(CSV_FILE)

    latest = df.iloc[-1]

    fault_probs = [
        latest["Healthy %"] / 100,
        latest["Bearing %"] / 100,
        latest["Imbalance %"] / 100,
        latest["Misalignment %"] / 100,
        latest["Critical %"] / 100
    ]

    fault_classes = [
        "Healthy",
        "Bearing",
        "Imbalance",
        "Misalignment",
        "Critical"
    ]

    sorted_probs = sorted(
        zip(fault_classes, fault_probs),
        key=lambda x: x[1],
        reverse=True
    )

    top_fault = sorted_probs[0]

    styles = getSampleStyleSheet()

    heading = styles["Heading2"]

    normal = styles["BodyText"]

    cover_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=28,
        leading=35,
        spaceAfter=20
    )

    cover_sub = ParagraphStyle(
        "CoverSub",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=18,
        textColor=colors.darkblue
    )

    center = ParagraphStyle(
        "Center",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=12,
        leading=22
    )

    caption_style = ParagraphStyle(
        "Caption",
        parent=normal,
        alignment=TA_CENTER,
        fontSize=11,
        textColor=colors.darkblue,
        spaceAfter=8
    )

    obs_style = ParagraphStyle(
        "Observation",
        parent=normal,
        backColor=colors.whitesmoke,
        borderColor=colors.darkblue,
        borderWidth=0.5,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=12
    )

    story=[]

    story.append(Spacer(1,1*inch))

    story.append(
        Paragraph(
            "INDUSTRIAL<br/>PREDICTIVE MAINTENANCE SYSTEM",
            cover_title
        )
    )

    story.append(
        Paragraph(
            "Machine Health Report",
            cover_sub
        )
    )

    line = Drawing(450,10)
    line.add(Line(0,5,450,5))
    line.hAlign = "CENTER"
    story.append(Spacer(1,0.7*inch))
    story.append(line)
    story.append(Spacer(1,0.3*inch))

    story.append(
        Paragraph(
            "AI Powered Predictive Maintenance using IoT, Signal Processing, Machine Learning and Cloud Computing",
            center
        )
    )

    story.append(Spacer(1,0.8*inch))

    story.append(
        Paragraph(
            f"<b>Plant :</b> UVCE Smart Factory",
            center
        )
    )

    story.append(
        Paragraph(
            f"<b>Machine ID :</b> MTR-001",
            center
        )
    )

    story.append(
        Paragraph(
            f"<b>Location :</b> Bangalore",
            center
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated :</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            center
        )
    )

    story.append(Spacer(1,0.5*inch))

    if latest["Status"] == "HEALTHY":
        color = "green"
        status_text = "HEALTHY"

    elif latest["Status"] == "WARNING":
        color = "orange"
        status_text = "WARNING"

    else:
        color = "red"
        status_text = "CRITICAL"

    story.append(
        Paragraph(
            f'<font color="{color}" size="22"><b>{status_text}</b></font>',
            center
        )
    )  
    
    story.append(Spacer(1,1.2*inch))

    story.append(

        Paragraph(

            "Prepared by Industrial Predictive Maintenance System",

            center

        )

    )

    story.append(

        Paragraph(

            "Version 1.0",

            center

        )

    )

    story.append(

        Paragraph(

            "Confidential Report",

            center

        )

    )
    story.append(PageBreak())

    blue_heading = ParagraphStyle(
        "BlueHeading",
        parent=heading,
        textColor=colors.darkblue,
        fontSize=18,
        spaceAfter=10
    )
    
    story.append(
       Paragraph(
            "EXECUTIVE SUMMARY",
            blue_heading
        )
    )

    story.append(Spacer(1,0.25*inch))

    company_data = [

        ["Plant", "UVCE Smart Factory"],

        ["Machine ID", "MTR-001"],

        ["Report Date", datetime.now().strftime("%d-%m-%Y")],

        ["Generated Time", datetime.now().strftime("%H:%M:%S")]

    ]

    company_table = Table(company_data,colWidths=[2.3*inch,3.7*inch])

    company_table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#E8EEF7")),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

        ("BOTTOMPADDING",(0,0),(-1,-1),8),

    ]))

    story.append(company_table)

    story.append(Spacer(1,0.3*inch))

    status = latest["Status"]

    if status == "HEALTHY":

        colour = colors.green
        operating = "RUNNING"
        risk = "LOW"
        maintenance = "Routine Inspection"
        response = "30 Days"

    elif status == "WARNING":

        colour = colors.orange
        operating = "RUNNING WITH CAUTION"
        risk = "MEDIUM"
        maintenance = "Preventive Maintenance"
        response = "Within 7 Days"

    else:

        colour = colors.red
        operating = "STOP IMMEDIATELY"
        risk = "HIGH"
        maintenance = "Corrective Maintenance"
        response = "Immediate"

    summary = [

        ["Parameter","Current Value"],

        ["Temperature",f"{latest['Temperature']} °C"],

        ["RMS",f"{latest['RMS']}"],

        ["Peak",f"{latest['Peak']}"],

        ["Health Score",f"{latest['Health Score']} %"],

        ["Efficiency",f"{latest['Efficiency']} %"],

        ["Remaining Useful Life",f"{latest['Remaining Useful Life']} %"],

        ["OVERALL MACHINE STATUS",status]

    ]

    table = Table(summary,colWidths=[3*inch,3*inch])

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(0,-1),colors.HexColor("#F4F4F4")),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,-1),8)

    ]))

    table.setStyle(TableStyle([

        ("BACKGROUND", (-2,-1), (-1,-1), colour),

        ("TEXTCOLOR", (-2,-1), (-1,-1), colors.white),

        ("FONTNAME", (-2,-1), (-1,-1), "Helvetica-Bold")

    ]))

    story.append(table)

    story.append(Spacer(1,0.35*inch)) 

    fault_description = {

        "Healthy": "No Fault Detected",

        "Bearing": "Bearing Wear",

        "Imbalance": "Rotor Imbalance",

        "Misalignment": "Shaft Misalignment",

        "Critical": "Severe Machine Failure"

    }

    fault_table_data = [

        ["Fault", "Confidence"]

    ]

    for i, (cls, prob) in enumerate(sorted_probs):

        if prob > 0:
            bar = "█" * max(1, int(prob * 20))
        else:
            bar = ""

        if i == 0:
            fault_name = f"<b>{fault_description.get(cls, cls)}</b>"
        else:
            fault_name = fault_description.get(cls, cls)

        fault_table_data.append([
            Paragraph(fault_name, normal),
             Paragraph(
                f"<font face='Courier'>{bar:<20} {prob*100:.1f}%</font>",
                normal
            )
        ])

    fault_table = Table(
        fault_table_data,
        colWidths=[3.4*inch,2.6*inch]
    )

    fault_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,1),(0,-1),colors.whitesmoke),
        ("ALIGN",(0,0),(-1,0),"CENTER"),
        ("ALIGN",(0,1),(0,-1),"LEFT"),
        ("ALIGN",(1,1),(1,-1),"LEFT"),
        ("FONTNAME",(1,1),(1,-1),"Courier-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,-1),8)

    ]))

    story.append(
        Paragraph(
            "AI Fault Probability Analysis",
            blue_heading
        )
    )

    story.append(fault_table)

    story.append(Spacer(1,0.20*inch))

    top_fault = sorted_probs[0]

    story.append(
        Paragraph(
            f"""
            <b>AI Conclusion</b><br/><br/>
            
            Based on the machine health indicators and vibration features,
            the AI model predicts <b>{fault_description.get(top_fault[0], top_fault[0])}</b>
            as the most probable fault with an overall confidence of
            <b>{top_fault[1]*100:.1f}%</b>.

            The remaining fault probabilities are comparatively lower,
            indicating strong confidence in the predicted machine fault.
            """,
            normal
        )
    )

    story.append(Spacer(1,0.30*inch))
    story.append(PageBreak())

    fault =  top_fault[0]
    fault = fault.strip()

    root_cause = {

    "Healthy":
    "No abnormal operating behaviour observed. Machine is operating within <b>safe vibration and temperature</b> limits.",

    "Bearing":
    "High RMS vibration together with increasing high-frequency components indicates probable <b>bearing degradation</b>.",

    "Imbalance":
    "Periodic vibration amplitude suggests <b>rotor mass imbalance</b> requiring balancing.",

    "Misalignment":
    "Elevated temperature combined with abnormal peak vibration indicates possible <b>shaft misalignment</b>.",

    "Critical":
    "Multiple critical parameters exceeded safe operating limits indicating <b>imminent equipment failure</b>."

    }

    story.append(
        Paragraph(
            "<b>Root Cause Analysis</b>",
            blue_heading
        )
    )

    story.append(
        Paragraph(
            f"<b>Most Probable Fault:</b> " 
            f"{fault_description.get(top_fault[0], top_fault[0])} "
            f"({top_fault[1]*100:.1f}% confidence)",
            normal
        )
    )

    story.append(Spacer(1,0.12*inch))

    story.append(
        Paragraph(
            root_cause.get(
                fault,
                "No significant abnormality detected."
            ),
            normal
        )
    )

    story.append(
        Paragraph(
            "Machine Status Reference",
            blue_heading
        )
    )

    reference_data = [

    [
    "Status",
    "Health Score",
    "Operating State",
    "Response Time",
    "Maintenance"
    ],

    [
    "HEALTHY",
    "80-100%",
    "RUNNING",
    "30 Days",
    "Routine Inspection"
    ],

    [
    "WARNING",
    "60-79%",
    "RUNNING WITH CAUTION",
    "Within 7 Days",
    "Preventive Maintenance"
    ],

    [
    "CRITICAL",
    "<60%",
    "STOP IMMEDIATELY",
    "Immediate",
    "Corrective Maintenance"
    ]

    ]

    reference_table = Table(
        reference_data,
        colWidths=[
            1.2*inch,
            1.0*inch,
            1.7*inch,
            1.0*inch,
            1.6*inch
        ]
    )

    reference_table.setStyle(TableStyle([

    ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

    ("BACKGROUND",(0,1),(-1,1),colors.HexColor("#D9F2D9")),   # Green
    ("BACKGROUND",(0,2),(-1,2),colors.HexColor("#FFF4CC")),   # Yellow
    ("BACKGROUND",(0,3),(-1,3),colors.HexColor("#F8D7DA")),   # Red

    ("GRID",(0,0),(-1,-1),1,colors.grey),

    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

    ("ALIGN",(0,0),(-1,-1),"CENTER"),

    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

    ("BOTTOMPADDING",(0,0),(-1,-1),8),

    ("TOPPADDING",(0,0),(-1,-1),8)

    ]))

    story.append(reference_table)

    story.append(Spacer(1,0.35*inch))

    story.append(
        Paragraph(
            "<b>AI Assessment</b>",
            blue_heading
        )
    )

    if latest["Status"] == "HEALTHY":
        status_color = "green"
    elif latest["Status"] == "WARNING":
        status_color = "orange"
    else:
        status_color = "red"
    
    story.append(
        Paragraph(
            f"""
            The Industrial Predictive Maintenance System continuously analyses
            vibration signals, temperature trends and machine health indicators to
            identify early signs of equipment degradation and potential failures.

            <br/><br/>

            <b>Rule Engine Status:</b>
            <font color="{status_color}"><b>{latest['Status']}</b></font>

            <br/><br/>

            <b>AI Prediction:</b>
            <b>{latest['AI Prediction']}</b>
            ({latest['Confidence']:.1f}% confidence)

            <br/><br/>

            <b>Predicted Fault:</b>
            <b>{fault_description.get(top_fault[0], top_fault[0])}</b>
            ({top_fault[1]*100:.1f}% confidence)

            <br/><br/>

            <b>Final Machine Status:</b>
            <font color="{status_color}"><b>{latest['Status']}</b></font>

            <br/><br/>

            The rule engine remains the final safety authority.
            AI predictions are used to detect early degradation but cannot override
            critical safety rules.

            <br/><br/>

            Current machine health is estimated at
            <b>{latest['Health Score']:.1f}%</b>, with an estimated remaining useful
            life of <b>{latest['Remaining Useful Life']:.1f}%</b>.
            """,
            normal
        )
    )

    story.append(Spacer(1,0.35*inch))

    story.append(
        Paragraph(
            "<b>Recommended Action</b>",
            blue_heading
        )
    )

    if latest["Status"]=="HEALTHY":

        action="""
        Machine operating under normal conditions.
        Continue monitoring and perform routine inspection after 30 days.
        """

    elif latest["Status"]=="WARNING":

        action="""
        Early signs of abnormal vibration detected.
        Inspect bearings, lubrication and shaft alignment within 7 days.
        """

    else:

        action="""
        Critical vibration detected.
        Immediate shutdown is recommended.
        Inspect shaft alignment, bearings and rotating components before restarting.
        Resume operation only after maintenance verification.
        """

    story.append(Paragraph(action,normal))

    story.append(PageBreak())


    story.append(
        Paragraph(
            "Sensor Trend Analysis",
            blue_heading
        )
    )

    story.append(
        Paragraph(
           """
           The following graphs illustrate the recent behaviour of the monitored
            machine. Historical trends help engineers identify degradation,
            abnormal vibration patterns and thermal anomalies before failure.
            """,
            normal
        )
    )

    story.append(Spacer(1,0.2*inch))

    graph_observations = {

        "temperature_history.png":
        "Temperature trend indicates thermal behaviour of the machine over recent operating cycles. Sudden increases may indicate overheating.",

        "rms_history.png":
        "RMS vibration values represent the overall vibration severity. Increasing RMS usually indicates bearing wear or imbalance.",

        "peak_history.png":
        "Peak values capture sudden impacts or transient faults occurring during machine operation.",

        "health_history.png":
        "Health score is calculated from vibration, temperature and fault indicators. Higher values indicate healthier operation.",

        "efficiency_history.png":
        "Machine efficiency estimates operational performance. Lower efficiency generally accompanies deteriorating machine health.",

        "rul_history.png":
        "Remaining Useful Life (RUL) estimates the expected operational life before maintenance becomes necessary.",

        "status_history.png":
        "Machine status trend shows transitions between Healthy, Warning and Critical operating states over time.",

        "healthy_signal.png":
        "Healthy vibration signal exhibits smooth periodic behaviour with minimal noise.",

        "fault_signal.png":
        "Faulty vibration signal contains abnormal oscillations introduced by simulated mechanical faults.",

        "filtered_signal.png":
        "Signal filtering removes measurement noise while preserving important vibration characteristics.",

        "temperature.png":
        "Temperature profile represents the machine's operating temperature during data acquisition.",

        "fft.png":
        "FFT identifies dominant vibration frequencies useful for detecting bearing wear, shaft misalignment and rotor imbalance."

    }

    graph_list=[
        
    ("temperature_history.png",
     "Figure 5.1 : Temperature History"),

    ("rms_history.png",
     "Figure 5.2 : RMS Vibration Trend"),

    ("peak_history.png",
     "Figure 5.3 : Peak Amplitude History"),

    ("health_history.png",
     "Figure 5.4 : Machine Health Trend"),

    ("efficiency_history.png",
     "Figure 5.5 : Machine Efficiency"),

    ("rul_history.png",
     "Figure 5.6 : Remaining Useful Life"),

    ("status_history.png",
     "Figure 5.7 : Machine Status History"),

    ("healthy_signal.png",
     "Figure 5.8 : Healthy Vibration Signal under Normal Operation"),

    ("fault_signal.png",
     "Figure 5.9 : Faulty Machine Signal"),

    ("filtered_signal.png",
     "Figure 5.10 : Filtered Signal"),

    ("temperature.png",
     "Figure 5.11 : Temperature Curve"),

    ("fft.png",
     "Figure 5.12 : Frequency Spectrum obtained using FFT")

    ]

    graph_counter = 0

    for graph, caption in graph_list:

        path = os.path.join(GRAPH_DIR, graph)

        if os.path.exists(path):

            graph_counter += 1

            story.append(
                Paragraph(
                    caption,
                    caption_style
                )
              )
            
            story.append(
                Image(
                    path,
                    width=6.3*inch,
                    height=3.2*inch
                )
            )

            story.append(
                Paragraph(
                    f"<b>Engineering Observation</b><br/>{graph_observations[graph]}",
                    obs_style
                )
            )

            d = Drawing(500,10)
            d.add(Line(0,5,500,5))
            story.append(d)

            story.append(
                Spacer(1,0.20*inch)
            )

    story.append(PageBreak())

    story.append(Spacer(1,1.3*inch))

    story.append(
        Paragraph(
            "END OF REPORT",
            cover_title
        )
    )

    story.append(Spacer(1,0.5*inch))

    story.append(
        Paragraph(
            "Generated automatically by the",
            center
        )
    )

    story.append(
        Paragraph(
            "<b>Industrial Predictive Maintenance System</b>",
            center
        )
    )

    story.append(Spacer(1,0.4*inch))

    story.append(
        Paragraph(
            "Version 1.0",
            center
        )
    )

    story.append(
        Paragraph(
            "© 2026",
            center
        )
    )

    story.append(
        Paragraph(
            "Confidential Report",
            center
        )
    )  

    line = Drawing(300,10)
    line.add(Line(0,5,300,5))

    line.hAlign = "CENTER"
    story.append(Spacer(1,0.15*inch))
    story.append(line)

    story.append(Spacer(1,0.25*inch))

    story.append(
        Paragraph(
            "This report was generated automatically using<br/>"
            "real-time sensor measurements, signal processing<br/>"
            "and AI-based predictive analytics.",
            center
        )
    ) 

    doc.build(
        story,
        canvasmaker=NumberedCanvas
        )
    buffer.seek(0)
    return buffer
