import "../CSS/footer.css"

function Footer(){
    return(
        <div className="grid-container-footer">
            <div className="grid-item-footer company-info-container">
                <p className="info-item">COMPANY ADDRESS: 124 Conch Street, Bikini Bottom, Pacific Ocean</p>
                <p className="info-item">PHONE NUMBER: 454-090-9999</p>
                <p className="info-item">COMPANY EMAIL: flatbook@fltbk.edu</p>
                <p className="info-item">LINKEDIN: flatbook@linkedin.com</p>
            </div>
            <div className="grid-item-footer vertical-line"></div>
            <div className="grid-item-footer legal-container">
                <p className="legal-item">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed in quam eu nunc mattis porttitor. Donec laoreet neque at lacus mattis, non mollis massa dictum. Sed ac ex in tellus varius elementum sed non ante. Mauris iaculis felis sed auctor interdum. Vivamus sed nibh id risus tincidunt pellentesque. Donec vitae ipsum ultrices, fermentum neque nec, finibus neque. Interdum et malesuada fames ac ante ipsum primis in faucibus. Phasellus quis cursus urna, a volutpat mauris. Ut quis augue pulvinar, pretium ante eu, ullamcorper nunc. Fusce blandit, massa vel accumsan tristique, neque sapien suscipit felis, sed fermentum lacus nisl non tortor. Praesent rutrum justo odio. Sed urna nunc, convallis id dolor vel, ultricies luctus velit.</p>
            </div>
        </div>
    )
}

export default Footer